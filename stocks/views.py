from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from stocks.models import Stocks
from stocks.forms import registration_form
from stocks.stocks import Stock

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
            user.profile.purse = INITIAL_AMOUNT
            login(request, user)
            return redirect("dashboard")
    else:
        form = registration_form()
    context = {"form":form}
    return render(request,"signup.html", context)

@login_required
def dashboard(request):
    stocks = [Stock("GOOGL"), Stock("AAPL"), Stock("MSFT")]
    context = {'user_stocks':stocks}
    return render(request, "UI/dashboard.html", context)

@login_required
def view_stock(request, slug):
    context = {"stock":get_object_or_404(Stocks, slug=name)}
    return render_to_response("stock.html", context)
