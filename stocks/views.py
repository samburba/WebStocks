from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from stocks.models import Stock, Owned_Stock
from stocks.forms import registration_form
from stocks.stocks import Stock as S
from decimal import Decimal
from stocks.models import Stock

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
            for s in Stock.objects.all():
                add_stock = Owned_Stock(user=created, stock=s)
                add_stock.save()
                created.stocks.add(add_stock)
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
    context = {'stocks':to_return_stocks    }
    return render(request, "UI/dashboard.html", context)

@login_required
def more(request):
    context = {'stocks':Stock.objects.all()}
    return render(request, "UI/more.html", context)

@login_required
def view_stock(request, slug):
    user = request.user
    stock = get_object_or_404(Stock, slug=slug)
    owned = user.profile.stocks.get(stock=stock)
    info = S(stock.slug)
    s_price = info.get_price()
    errors = []
    if request.method == 'POST':
        if "Buy" in request.POST:
            if user.profile.purse >= Decimal(s_price):
                owned.quantity += 1
                user.profile.purse -= Decimal(round(s_price, 2))
                user.profile.purse = Decimal(round(user.profile.purse,2))
            else:
                errors.append(user.get_username() + " does not have enough money for " + str(stock))
        elif "Sell" in request.POST:
            if owned.quantity > 0:
                owned.quantity -= 1
                user.profile.purse += Decimal(round(s_price, 2))
                user.profile.purse = Decimal(round(user.profile.purse,2))
            else:
                errors.append(user.get_username() + " does not have stock " + str(stock))
        owned.save()
        user.save()
        print(errors)
    context = {'s_name' : stock.slug, 's_full_name' : stock.full_name,
     's_price':s_price, 's_difference':info.get_percent_difference()}
    return render(request, "UI/stock.html", context)
