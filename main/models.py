from django.db import models
from django.contrib import admin
# Create your models here.

class UserRegistration(models.Model):
    username = models.CharField(max_length=100, primary_key=True, blank=False)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','password')


class UserDetails(models.Model):
    username = models.CharField(max_length=100, primary_key=True, blank=False)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phoneno = models.CharField(max_length=100)
    bio = models.CharField(max_length=1000)

class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('username','fname','lname','email','phoneno','bio')
    

class Portfolio(models.Model):
    portfolioname = models.CharField(max_length=100, primary_key=True, blank=False)
    username = models.ForeignKey(UserRegistration, max_length=100, blank=False, on_delete=models.CASCADE)

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('portfolioname', 'username')
    

class StockPortfolio(models.Model):
    portfoliostockid = models.CharField(max_length=100, primary_key=True, blank=False)
    username = models.ForeignKey(UserRegistration, max_length=100, blank=False, on_delete=models.CASCADE)
    portfolioname = models.ForeignKey(Portfolio, max_length=100, blank=False, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    companyname = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    exchangetype = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    targetprice = models.CharField(max_length=100)

class StockPortfolioAdmin(admin.ModelAdmin):
    list_display = ('portfoliostockid', 'username','portfolioname','date','companyname','type','exchangetype','quantity','price','targetprice')

class MutualFundPortfolio(models.Model):
    portfoliomfid = models.CharField(max_length=100, primary_key=True, blank=False)
    username = models.ForeignKey(UserRegistration, max_length=100, blank=False, on_delete=models.CASCADE)
    portfolioname = models.ForeignKey(Portfolio, max_length=100, blank=False, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    units = models.CharField(max_length=100)
    nav = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    foliono = models.CharField(max_length=100)

class MutualFundPortfolioAdmin(admin.ModelAdmin):
    list_display = ('portfoliomfid', 'username', 'portfolioname','date','type','units','nav','amount','foliono')

class WatchList(models.Model):
    watchlistid = models.CharField(max_length=100, primary_key=True, blank=False)
    username = models.ForeignKey(UserRegistration, max_length=100, blank=False, on_delete=models.CASCADE)
    addeddate = models.CharField(max_length=100)
    addedprice = models.CharField(max_length=100)
    company = models.CharField(max_length=100)

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('watchlistid','username','addeddate','addedprice','company')


admin.site.register(UserRegistration, UserRegistrationAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(StockPortfolio, StockPortfolioAdmin)
admin.site.register(MutualFundPortfolio, MutualFundPortfolioAdmin)
admin.site.register(WatchList, WatchlistAdmin)
admin.site.register(UserDetails,UserDetailsAdmin)