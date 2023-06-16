from rest_framework import serializers
from django.contrib.auth.models import User
from . import models
from django.http import JsonResponse

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('id', 'username', 'email')
    def getId(self):
        return self.id
        
class StockSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Stock
        fields = ( 'name', 'symbol')  

  
        

class PortfolioSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta(object):
        model = models.Portfolio
        #TODO usiamo il tipo per simulare il risk management
        #se ho tempo di aggiungerlo
        fields = ('user', 'name', 'type')
    def getName(self):
        return self.name
    def getUser(self):
        return self.user
    def tickerList(self):
        self.user = UserSerializer(self.context.get('user'))
        self.portfolio = PortfolioSerializer(self.instance)
        self.tickers_set = models.Ticker.objects.filter(portfolio=self.instance)
        response_data = {
            
            'portfolio': self.portfolio.data,
            'tickers': SimpleTickerSerializer(self.tickers_set, many=True, ).data
        }
        return JsonResponse(response_data)
    
        
class PortfoliosSerializer(serializers.ModelSerializer):
    
    #PortfolioSerializer(many=True)
    #user = PortfolioSerializer().getUser() 
    
    portfolios_set = PortfolioSerializer(many=True)
    #TODO ritornare all'inizio l'user e poi la lista dei nomi del portafoglio che ha
    
    class Meta(object):
        model = User
        fields = ( 'username','email', 'portfolios_set' )
        
    def portfolioList(self):
        self.user = UserSerializer(self.instance)
        portfolios_set = models.Portfolio.objects.filter(user=self.context.get('instance'))
        self.portfolios_set = portfolios_set
        response_data = {
            'user': self.user.data,
            'portfolios': [Portfolio.name for Portfolio in self.portfolios_set]
        }
        return JsonResponse(response_data)
    
    
        
        
class TickerSerializer(serializers.ModelSerializer):
    portfolio = PortfolioSerializer()
    class Meta(object):
        model = models.Ticker
        fields = ('portfolio', 'stock', 'shares', 'price')  
        
class SimpleStockSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = models.Stock
        fields = (  'symbol' ,)
    def getSymbol(self):
        return self.data['symbol']  
        
class SimpleTickerSerializer(serializers.ModelSerializer):
    stockSymbol = serializers.CharField(source='stock.symbol')
    class Meta(object):
        model = models.Ticker
        fields = ('stockSymbol', 'shares', 'price')


        

        
