from . import views
from django.urls import path


urlpatterns = [
    path('register/', views.register, name="register"),
	path('login/', views.login, name="login"),  
	

    path('',views.index,name='index'),
    path('news/',views.news,name='news'),
    path('addportfolio/',views.addportfolio,name='addportfolio'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('stock/',views.Stock,name='stock'),
    path('Mutualfunds/',views.mutualfund,name='mutualfunds'),
    path('watchlist/',views.watchlist,name='watchlist'),
    path('settings/',views.settings,name='settings'),
    path('signup/',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('portfolioadd',views.addportfolioname,name='addportfolioname'),
    path('addstock',views.addstock,name="addstock"),
    path('addmf',views.addmf,name="addmf"),
    path('topgainers',views.topgainers,name="topgainers"),
    path('toplosers',views.toplosers,name="toplosers"),
    path('getstockdata',views.stockdata,name="stockdata"),
    path('addscripwatchlist',views.addscripwatchlist,name="addscripwatchlist"),
    path('getprice',views.getprice,name="getprice"),
    path('updatepassord',views.updatepassord,name="updatepassord"),
    path('updateuserdetails',views.updateuserdetails,name="updateuserdetails"),
    path('logout',views.logout,name="logout"),
]
