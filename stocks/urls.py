#contiene gli url dell'applicazione stocks
from django.urls import path
from .views import homePageView
from django.urls import include
from . import views

urlpatterns = [
    path('', homePageView, name='home'),
    path('stock/', views.stockPageView, name='stock'),
    path('stock/<str:symbol>', views.stockDetailView, name='stock'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('test_token/', views.test_token, name='test_token'),
    path('yahooTest/', views.yahooTestView, name='yahooTest'),
    path('createPortfolio/', views.createPortfolio, name='createPortfolio'),
    path('portfolio/', views.portfolioView, name='portfoliodetails'),
    path('portfolioDetails/', views.portfolioDetailsView, name='portfoliodetails'),
    path('allportfolios/', views.allPortfoliosView, name='allportfolios'),
    path('addTicker/', views.addTickertoPortfolio, name='addticker'),
    path('removeTicker/', views.removeTickerfromPortfolio, name='removeticker'),
    path('ticker/<str:symbol>', views.tickerView, name='ticker'),
]