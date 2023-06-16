from django.db import models

# Create your models here.


class Stock(models.Model):
    #campi del modello
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=10)
    
    
    def Stock(self, symbol, name):
        self.symbol = symbol
        self.name = name
        

    #metodo che ritorna il nome del modello
    def __str__(self):
        return self.name

#TODO createPortfolio rende vuoti nome e tipo e rende la chiave di user
class Portfolio(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    username = models.CharField(max_length=200, default='')
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    def __str__(self):
        return self.name    
    

class Ticker(models.Model):
    #relazione uno a molti con il modello Stock e Portfolio
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    stockSymbol = models.CharField(max_length=10)
    shares = models.IntegerField()
    price = models.FloatField()
    
    #metodo che ritorna il nome del modello
    def __str__(self):
        return self.stock.symbol + " " + self.shares.__str__() + " " + self.price.__str__()
    
# class Quote(models.Model):
#     stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
#     date = models.DateField()
#     open = models.FloatField()
#     high = models.FloatField()
#     low = models.FloatField()
#     close = models.FloatField()
#     volume = models.IntegerField()
    
#     #metodo che ritorna il nome del modello
#     def __str__(self):
#         return self.name
    

