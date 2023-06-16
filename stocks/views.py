from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy 
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import status
from .serializer import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

#comodissimo perchè se non trova l'oggetto ritorna una 404 automaticamente
from django.shortcuts import get_object_or_404
#con questi import  possiamo verificare le sessioni con il token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

import finnhub
import json
import yfinance as yf

apiKeyClear = "chtjqghr01qvn1d2nrs0chtjqghr01qvn1d2nrsg"

# Create your views here.
def homePageView(request):
    return HttpResponse('<h1>Hello, World!</h1>')


def yahooTestView(request):
    msft = yf.Ticker("MSFT")
    return HttpResponse('<h1>Yahoo Test</h1><p>'+str(msft.info)+'</p>')

def stockPageView(request):
    finnhub_client = finnhub.Client(api_key=apiKeyClear)
    stockSymbolLookup = finnhub_client.symbol_lookup('AAPL')
    print(stockSymbolLookup)
    return HttpResponse('<h1>Stock Page</h1><p>Symbol Lookup</p><p>'+str(stockSymbolLookup)+'</p>')

@api_view(['GET'])
def stockDetailView(request,symbol):
    stockDetails = yf.Ticker(symbol).get_info()
    stock = models.Stock(symbol=symbol, name=stockDetails['longName'])
    serializer = StockSerializer(instance = stock)
    return Response({"data" : serializer.data}, status=status.HTTP_202_ACCEPTED)


# @api_view(['GET'])
# @authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
# def portfolioView(request):
#     return HttpResponse('<h1>Portfolio Page of user'+request.user.username+'</h1>')

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def tickerView(request,symbol):
    ticker = yf.Ticker(symbol)
    serializer = TickerSerializer(ticker.info)
    return Response(ticker.info)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def createPortfolio(request):
    if(models.Portfolio.objects.filter(name=request.data['name']).exists()):
        return Response({"detail": "Portfolio name already exists."}, status=status.HTTP_400_BAD_REQUEST)
    portfolio = models.Portfolio(user=request.user, name=request.data['name'], type=request.data['type'])
    portfolio.save()
    serializer = PortfolioSerializer(instance = portfolio)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def portfolioView(request):
    if(not models.Portfolio.objects.filter(name=request.data['name']).exists()):
        return Response({"detail": "Portfolio name does not exists."}, status=status.HTTP_400_BAD_REQUEST)
    portfolios = models.Portfolio.objects.filter(user=request.user)
    portfolio = get_object_or_404(portfolios, name=request.data['name'])
    serializer = PortfolioSerializer(instance = portfolio)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def allPortfoliosView(request):
    #portfolios = models.Portfolio.objects.filter(user=)
    serializer = PortfoliosSerializer(instance = request.user,context={'instance': request.user})
    return HttpResponse(serializer.portfolioList(), status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def portfolioDetailsView(request):
    if(not models.Portfolio.objects.filter(name=request.data['name']).exists()):
        return Response({"detail": "Portfolio name does not exists."}, status=status.HTTP_400_BAD_REQUEST)
    portfolios = models.Portfolio.objects.filter(user=request.user)
    portfolio = get_object_or_404(portfolios, name=request.data['name'])
    serializer = PortfolioSerializer(instance = portfolio,context={'user': request.user})
    return HttpResponse(serializer.tickerList(), status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def addTickertoPortfolio(request):
    portfolio = get_object_or_404(models.Portfolio, name=request.data['name'], user = request.user)
    #TODO controllare che il ticker non sia già presente nel portfolio
    #TODO modificare il modo in cui otteniamo Stock(in base al fatto se salviamo i symbol o no)
    stock = get_object_or_404(models.Stock, symbol=request.data['symbol'])
    ticker = models.Ticker(portfolio=portfolio, stock=stock, shares=request.data['shares'], price=request.data['price'])
    ticker.save()
    serializer = TickerSerializer(instance = ticker)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def removeTickerfromPortfolio(request):   
    portfolio = get_object_or_404(models.Portfolio, name=request.data['name'], user = request.user)
    stock = get_object_or_404(models.Stock, symbol=request.data['symbol'])
    portfolio_tickers = models.Ticker.objects.filter(portfolio=portfolio)
    lenght = 0
    try:
        ticker = get_object_or_404(portfolio_tickers, stock = stock, shares=request.data['shares'], price=request.data['price'])
    except models.Ticker.MultipleObjectsReturned:
        lenght = len(models.Ticker.objects.filter(portfolio=portfolio, stock = stock, shares=request.data['shares'], price=request.data['price']))
        ticker = models.Ticker.objects.filter(portfolio=portfolio, stock = stock, shares=request.data['shares'], price=request.data['price'])[0]
        
    deleteResult = ticker.delete()
    if(deleteResult[0] == 0 ):
        return Response({"detail": "Ticker not deleted."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Ticker deleted."}, status=status.HTTP_202_ACCEPTED)

 

# viste per autenticazione #   

@api_view(['POST'])
def login(request): 
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created= Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance = user)
    return Response({"token": token.key, "user": serializer.data})

@api_view(['POST'])
def signup(request): 
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        #salva l'utente nel database
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        #così non salva la password in chiaro ma la salva criptata
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request): 
    return Response("passed for {}".format(request.user.username))




