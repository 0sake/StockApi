from django.contrib import admin
from . import models

#username: admin password: polloroot email: itato0105@gmail.com

# Register your models here.

admin.site.register(models.Stock)

admin.site.register(models.Portfolio)

admin.site.register(models.Ticker)