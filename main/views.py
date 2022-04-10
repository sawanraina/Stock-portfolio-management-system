from django.shortcuts import render
from .models import *
from django.core.exceptions import *
from django.db import *
from django.http import JsonResponse
from .StockData import *
from datetime import *
import yfinance as yf
import numpy as np




def login(request):
    return render(request, 'login.html')

def signup(request):
    response_data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            UserRegistration.objects.create(
                username = username,
                email = email,
                password = password,
            )
            response_data['success'] = "Account Created"
            return JsonResponse(response_data)
        except IntegrityError as e:
            print("Error Account Creating: "+str(e))
            response_data['error'] = str("Already Account Created")
            return JsonResponse(response_data)
        except Exception as e:
            print("Error Account Creating: "+str(e))
            response_data['error'] = str("Erorr occured")
            return JsonResponse(response_data)

def signin(request):
    response_data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            print(username,password)
            user_data = UserRegistration.objects.get(username=username,password=password)
            if(user_data):
                response_data['success'] = "Logged In Success"
                request.session['username'] = user_data.username
                dashboard(request)
            else:
                response_data['error'] = "Invalid Login"
        except ObjectDoesNotExist as e:
            response_data['error'] = "Invalid Login"
        except Exception as e:
            response_data['error'] = str(e)
        return JsonResponse(response_data)


def addportfolioname(request):
    response_data = {}
    if request.method == 'POST':
        portfolioname = request.POST.get('portfolioname')
        user = UserRegistration.objects.get(username=request.session['username'])
        try:
            Portfolio.objects.create(
                portfolioname = portfolioname,
                username = user,
            )
            response_data['success'] = "Portfolio Created"
            return JsonResponse(response_data)
        except IntegrityError as e:
            print("Error Portfolio Creating: "+str(e))
            response_data['error'] = str("Already Portfolio Created")
        except Exception as e:
            print("Error Portfolio Creating: "+str(e))
            response_data['error'] = str("Erorr occured")
            return JsonResponse(response_data)

def register(request):
    return render(request, 'register.html')

def index(request):
    return render(request, 'index.html')

def news(request):
    import requests
    import json
    api_request = requests.get("https://newsapi.org/v2/everything?q=stocks&sortBy=publishedAt&apiKey=eaee6b4ee6bb4dc1a1d6fa1d9de4387c")
    api = json.loads(api_request.content)
    return render(request, 'news.html', {'api' : api})

def addstock(request):
    response_data = {}
    if request.method == 'POST':
        portfolioname = Portfolio.objects.get(portfolioname = request.POST.get('portfolioname'))
        date = request.POST.get('date')
        companyname = request.POST.get('companyname')
        type = request.POST.get('type')
        exchangetype = request.POST.get('exchange')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        targetprice = request.POST.get('targetprice')
        try:
            StockPortfolio.objects.create(
                portfoliostockid = str(request.session['username'])+str(request.POST.get('portfolioname'))+str(companyname),
                username = UserRegistration.objects.get(username=request.session['username']),
                portfolioname = portfolioname,
                date = date,
                companyname = companyname,
                type = type,
                exchangetype = exchangetype,
                quantity = quantity,
                price = price,
                targetprice = targetprice,
            )
            
            response_data['success'] = "Account Created"
            return JsonResponse(response_data)
        except IntegrityError as e:
            print("Error Account Creating: "+str(e))
            response_data['error'] = str("Already Account Created")
        except Exception as e:
            print("Error Account Creating: "+str(e))
            response_data['error'] = str("Erorr occured")
            return JsonResponse(response_data)

def addmf(request):
    response_data = {}
    if request.method == 'POST':
        portfolioname = Portfolio.objects.get(portfolioname = request.POST.get('portfolioname'))
        date = request.POST.get('date')
        type = request.POST.get('type')
        units = request.POST.get('units')
        nav = request.POST.get('nav')
        amount = request.POST.get('amount')
        foliono = request.POST.get('foliono')

        try:
            MutualFundPortfolio.objects.create(
                portfoliomfid = str(request.session['username'])+str(request.POST.get('portfolioname'))+str(foliono),
                username = UserRegistration.objects.get(username=request.session['username']),
                portfolioname = portfolioname,
                date = date,
                type = type,
                units = units,
                nav = nav,
                amount = amount,
                foliono = foliono,
            )
            
            response_data['success'] = "Account Created"
            return JsonResponse(response_data)
        except IntegrityError as e:
            print("Error Account Creating: "+str(e))
            response_data['error'] = str("Already Account Created")
        except Exception as e:
            print("Error Account Creating: "+str(e))
            response_data['error'] = str("Erorr occured")
            return JsonResponse(response_data)


def getprice(request):
    response_data = {}
    if request.method == 'POST':
        companyname = request.POST.get('companyname')
        startdate = request.POST.get('date')
        enddate = subtarctdays(startdate,1)
        print(date)
        try:
            data = yf.download(companyname+".NS", start=enddate, end=startdate)
            print(data)
            response_data['success'] = data['Close'][0]
        except Exception as e:
            print("Failed to Load: ",str(e))
            response_data['success'] = "Success"

    return JsonResponse(response_data)


def addscripwatchlist(request):
    response_data = {}
    if request.method == 'POST':
        username = UserRegistration.objects.get(username = request.session["username"])
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        symbol = request.POST.get('companyname')+".NS"
        stock = yf.Ticker(symbol)
        latest_price = stock.history(period='1d')['Close'][0]
        estimate = round(latest_price, 3) 
        try:
            WatchList.objects.create(
                watchlistid = str(request.session['username'])+str(request.POST.get('companyname')),
                username = username,
                addeddate = d1,
                addedprice = estimate,
                company = request.POST.get('companyname'),
            )
            
            response_data['success'] = "WatchList Added"
            return JsonResponse(response_data)
        except IntegrityError as e:
            print("Error WatchList Creating: "+str(e))
            response_data['error'] = str("Already Added")
        except Exception as e:
            print("Error WatchList Creating: "+str(e))
            response_data['error'] = str("Erorr occured")
            return JsonResponse(response_data)


def updatepassord(request):
    response_data = {}
    if request.method == "POST":
        oldpass = request.POST.get('oldpass');
        newpass = request.POST.get('newpass')

        try:
            user_data = UserRegistration.objects.get(username=request.session['username'])
            if user_data.password == oldpass:
                UserRegistration.objects.update(username=request.session['username'],password=newpass)
                response_data['success'] = "Password updated"
            else:
                response_data['error'] = "Old Password not Matching"
        except Exception as e:
            response_data['error'] = str(e)

    return JsonResponse(response_data)
    

    

def addportfolio(request):
    return render(request, 'Add Portfolio.html')

def dashboard(request):
    investmentCost = 0
    currentinvestmentCost = 0
    data = Portfolio.objects.filter(username=request.session['username'])
    username = request.session['username']
    stockdetails = StockPortfolio.objects.filter(username=request.session['username'])

    currentvaluation = 0.0
    totalinvested = 0.0
    for i in stockdetails:
        stock = yf.Ticker(i.companyname+".NS")
        stockcurrentinvestmentCost = stock.history(period='1d')['Close'][0]
        currentvaluation += float(stockcurrentinvestmentCost)*int(i.quantity)
        totalinvested += float(i.price)*int(i.quantity)

    notionallossgain = "{:.2f}".format(currentvaluation-totalinvested)
    currentvaluation = "{:.2f}".format(currentvaluation)
    totalinvested = "{:.2f}".format(totalinvested)
    

    allstock = {
        'currentvaluation':currentvaluation,
        'totalinvested':totalinvested,
        'notionalgainloss': notionallossgain
    }
    print(currentvaluation,totalinvested)




    stockportdetails = []
    for i in stockdetails:
        scripdata = yf.Ticker(i.companyname+".NS")
        currentinvestmentCost = scripdata.history(period='1d')['Close'][0]
        stock = {
            'companyname':i.companyname,
            'ltp': currentinvestmentCost,
            'quantity':i.quantity,
            'amountinvest': float(i.price)*float(i.quantity),
            'avginvest':float(i.price),
            'currentvoworth' : float(currentinvestmentCost)*float(i.quantity),
            'notionalgainloss' : float(currentinvestmentCost)-float(i.price)*int(i.quantity),
            'target':i.targetprice,
        }
        stockportdetails.append(stock)




    currentinvestmentCost = "{:.2f}".format(currentinvestmentCost)
    investmentCost = "{:.2f}".format(investmentCost)
    notional = float(currentinvestmentCost) - float(investmentCost)
    notional = "{:.2f}".format(notional)
    dashboardhead = {
    'investmentCost':totalinvested,
    'currentinvestmentCost':currentvaluation,
    'notionalcost': notionallossgain,
    }
    return render(request, 'Dashboard.html',{'portfoliodata':data,'username':username,'dashboardhead':dashboardhead,'stockdetails':stockportdetails,'allstock':allstock})

def Stock(request):
    allscrip = []
    try:
        nse = NSE()
        allscrip = nse.allscrip()
    except Exception as e:
        print("Connection Error NSE: ",e)
        response_data['error'] = "Connection Error"
        
    userData = {
    'allscripname':allscrip,
    }
    return render(request, 'Stock.html',{'data':userData})

def mutualfund(request):
    return render(request, 'Mutual Funds.html')

def watchlist(request):
    data = WatchList.objects.filter(username = request.session['username'])
    watchlistarr = []
    for i in data:
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        symbol = i.company+".NS"
        stock = yf.Ticker(symbol)
        latest_price = stock.history(period='1d')['Close'][0]
        estimate = round(latest_price, 2) 
        change = float(i.addedprice) - float(estimate)
        perchange = (change/float(i.addedprice))*100
        state,ema10,ema20 = checkstate(i.company)
        change =  "{:.2f}".format(change)
        perchange = "{:.2f}".format(perchange)
        watchlist = {
        "addeddate":i.addeddate,
        "addedprice":i.addedprice,
        "company":i.company,
        "liveprice":estimate,
        "change":change,
        "perchange":perchange,
        "state":state,
        "ema10":ema10,
        "ema20":ema20,
        }
        watchlistarr.append(watchlist)

    return render(request, 'watchlist.html',{'watchlistdata':watchlistarr})



def checkstate(scripname):
    today = date.today()

    stopDate = today.strftime("%Y-%m-%d")
    startDate = subtarctdays(stopDate,60)

    data = yf.download(scripname+".NS", start=startDate, end=stopDate)
    data['EMA10'] = data['Close'].ewm(span=10, adjust=False).mean()
    data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
    data['Position']  = np.where(data['EMA10'] > data['EMA20'], 1, 0)
    data['Signal'] = data['Position'].diff()
    status = data['Signal'][len(data)-1]
    if status == 0.0:
        status = "WAIT"
    elif status == 1.0:
        status = "BUY"
    else:
        status = "SELL"

    return status,data['EMA10'].tolist(),data['EMA20'].tolist()


def subtarctdays(startdate,days):
    date_format = '%Y-%m-%d'
    dtObj = datetime.strptime(startdate, date_format)
    past_date = dtObj - timedelta(days=days)
    past_date_str = past_date.strftime(date_format)
    return past_date


def updateuserdetails(request):
    response_data = {}
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio')

        print("Fname: ",fname," lName: ",lname," EMail: ",email," phone: ",phone," bio: ",bio)

        try:
            data = UserDetails.objects.filter(username=request.session['username'])
            if data:
                UserDetails.objects.update(username=request.session['username'],fname=fname,lname=lname,email=email,phoneno=phone,bio=bio)
            else:
                UserDetails.objects.create(username=request.session['username'],fname=fname,lname=lname,email=email,phoneno=phone,bio=bio)
            response_data['success'] = "Updated"
        except Exception as e:
            response_data['error'] = str(e)

    return JsonResponse(response_data)


def settings(request):
    data = UserDetails.objects.get(username=request.session['username'])
    print(data.bio)
    data = {
    'fname':data.fname,
    'lname':data.lname,
    'email':data.email,
    'phoneno':data.phoneno,
    'bio':data.bio
    }
    return render(request, 'settings.html',{'data': data})

def topgainers(response):
    response_data = {}
    try:
        nse = NSE()
        response_data['success'] = nse.topgainers()
        return JsonResponse(response_data)
    except ConnectionError as e:
        response_data['error'] = "Failed to Load"
        print("Connection Error: ",e)
        return JsonResponse(response_data)
    except Exception as e:
        print("Top Gainers Error: ",str(e))
        response_data['error'] = "Failed to Load"
        return JsonResponse(response_data)


def toplosers(response):
    response_data = {}
    try:
        nse = NSE()
        response_data['success'] = nse.toplosers()
        return JsonResponse(response_data)
    except ConnectionError as e:
        response_data['error'] = "Failed to Load"
        print("Connection Error: ", e)
        return JsonResponse(response_data)
    except Exception as e:
        print("Top Losers Error: ",str(e))
        response_data['error'] = "Failed to Load"
        return JsonResponse(response_data)


def stockdata(request):
    response_data = {}
    try:
        nse = NSE()
        scrip = request.POST.get('scripname');
        fromdate = request.POST.get('fromdate');
        enddate = request.POST.get('enddate');
        print(fromdate,enddate)
        response_data['success'] = nse.getscripdata(scrip,fromdate,enddate)
        return JsonResponse(response_data)
    except Exception as e:
        response_data['success'] = str(e)
        print("Error: ",e)
        return JsonResponse(response_data)

def logout(request):
    response_data = {}
    try:
        request.session['username'] = ""
        response_data['success'] = "Success Logout"
        return JsonResponse(response_data)
    except Exception as e:
        response_data['success'] = str(e)
        print("Error: ",e)
        return JsonResponse(response_data)