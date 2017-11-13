from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from stocks.forms import registration_form

# Create your views here.

TITLE = "Title"
def index(request):
    context = {'Title':TITLE}
    return render(request, "index.html", context)

def signup(request):
    if request.method == 'POST':
        form = registration_form(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request, user)
            return redirect("/")
    else:
        form = registration_form()
    context = {"form":form}
    return render(request,"signup.html", context)

def dashboard(request):
    context = {}
    return render(request, "UI/dashboard.html", context)
