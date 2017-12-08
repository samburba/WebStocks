#necessary:
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from stocks.models import Stock, Owned_Stock, Comment
from stocks.forms import registration_form, comment_form
from stocks.stocks import Stock as S
from decimal import Decimal
from stocks.models import Stock
#something from stack overflow:
from operator import attrgetter
#the AI :
from stocks.ai_viterbi import Viterbi
from stocks.ai_config import states, initial, trans, emiss, possible_obs
#necessary for the AI:

# Create your views here.

TITLE = "Title"
#The initial amount of starting money
INITIAL_AMOUNT = 1000

def index(request):
    context = {'Title':TITLE}
    return render(request, "index.html", context)

def signup(request):
    if request.method == 'POST':
        form = registration_form(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            created = user.profile
            created.purse = INITIAL_AMOUNT
            login(request, user)
            return redirect("dashboard")
    else:
        form = registration_form()
    context = {"form":form}
    return render(request,"signup.html", context)

@login_required
def dashboard(request):
    user = request.user
    stocks = user.profile.stocks.all()
    to_return_stocks = []
    for s in stocks:
        if s.quantity > 0:
            to_return_stocks.append(s)
    context = {'stocks':to_return_stocks}
    return render(request, "UI/dashboard.html", context)

@login_required
def leaderboard(request):
    users = User.objects.all()
    highest_to_lowest = []
    users_sorted = sorted(users, key=attrgetter('profile.estimated_net'))
    context = {"users" : users_sorted[::-1]}
    return render(request, "UI/leaderboard.html", context)

@login_required
def profile(request):
    context = {}
    return render(request, "UI/profile.html", context)

@login_required
def notfound(request):
    context = {}
    return render(request, "UI/notfound.html", context)


@login_required
def portfolio(request):
    user = request.user
    stocks = user.profile.stocks.all()
    evaluation = 0
    for s in stocks:
        evaluation += s.purchase_price
    total_evaluation = user.profile.purse + evaluation
    context = {"user":user, "stocks":stocks, "evaluation":evaluation, "total_evaluation":total_evaluation}
    return render(request, "UI/portfolio.html", context)

@login_required
def advisor(request):
    context = {"prediction":"Error", "error":True}
    if request.method == 'POST':
        if "Go" in request.POST and "Ticker" in request.POST:
                stock_name = request.POST["Ticker"]
                stock = S(stock_name)
                hist_prices = stock.get_week_prices()
                #Set up the VITERBI
                if hist_prices is not "Error":
                    obs = []
                    obs_prices = []
                    obs_delta = []
                    prev_price = hist_prices["Adj Close"][0]
                    for price in hist_prices["Adj Close"]:
                        if price >= prev_price:
                            obs.append("Up")
                        else:
                            obs.append("Down")
                        obs_prices.append(price)
                        obs_delta.append(price - prev_price)
                        prev_price = price
                    v = Viterbi(initial, states, obs, possible_obs, trans, emiss)
                    v.run()
                    backtrack = v.get_backtrack()
                    prediction = backtrack[-1]
                    context = {"stock":stock_name, "prediction":prediction.lower(), "error":False}
    return render(request, "UI/advisor.html", context)

@login_required
def more(request):
    context = {'stocks':Stock.objects.all()}
    return render(request, "UI/more.html", context)

#TODO: when the stock is 0 delete it from the user's Owned_Stock
@login_required
def view_stock(request, slug):
    user = request.user
    stock = get_object_or_404(Stock, slug=slug)
    has_stock = False
    quantity_owned = 0
    if user.profile.stocks.filter(stock=stock).exists():
        has_stock = True
        quantity_owned = user.profile.stocks.get(stock=stock).quantity
    info = S(stock.slug)
    s_price = info.get_price()
    errors = []
    #Buying and Selling stocks
    if request.method == 'POST':
        #If user is buying
        if "Buy" in request.POST:
            #If the user has enough money
            if user.profile.purse >= Decimal(s_price):
                #If they do not have the stock, put it in Owned_Stock
                if not has_stock:
                    created = user.profile
                    add_stock = Owned_Stock(user=created, stock=stock)
                    add_stock.save()
                    created.stocks.add(add_stock)
                    has_stock = True
                owned = user.profile.stocks.get(stock=stock)
                owned.quantity += 1
                owned.purchase_price = Decimal(round(s_price, 2))
                user.profile.purse -= Decimal(round(s_price, 2))
                user.profile.purse = Decimal(round(user.profile.purse,2))
            else:
                errors.append(user.get_username() + " does not have enough money for " + str(stock))
        #if user is selling
        elif "Sell" in request.POST:
            #make sure they have the stock and own more than 0
            if has_stock:
                owned = user.profile.stocks.get(stock=stock)
                if owned.quantity > 0:
                    owned.quantity -= 1
                    user.profile.purse += Decimal(round(s_price, 2))
                    user.profile.purse = Decimal(round(user.profile.purse,2))
                else:
                    errors.append(user.get_username() + " does not have stock " + str(stock))
            else:
                errors.append(user.get_username() + " does not have stock " + str(stock))
        owned.save()
        user.save()

        if has_stock:
            quantity_owned = user.profile.stocks.get(stock=stock).quantity
        print(errors)
    stocks = user.profile.stocks.all()
    evaluation = 0
    for s in stocks:
            evaluation += s.purchase_price
    total_evaluation = user.profile.purse + evaluation
    user.estimated_net = total_evaluation
    user.save()
    print(user.estimated_net)
    return_comments = []
    if Comment.objects.filter(stock=stock).exists():
        return_comments = Comment.objects.filter(stock=stock)
    context = {'s_name' : stock.slug, 's_full_name' : stock.full_name,
     's_price':s_price, 's_difference':info.get_percent_difference(), 'quantity_owned':quantity_owned,
     'comments':return_comments}
    return render(request, "UI/stock.html", context)

@login_required
def add_comment_to_stock(request, slug):
    stock = get_object_or_404(Stock, slug=slug)
    if request.method == "POST":
        form = comment_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.stock = stock
            comment.author = request.user
            comment.save()
            return redirect('/stocks/' +  slug)
    else:
        form = comment_form()
    return render(request, 'UI/add_comment_to_stock.html', {'form': form})
