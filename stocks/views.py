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
            form.save(commit=True)
            return redirect("/")
    else:
        form = registration_form()
    context = {"form":form}
    return render(request,"signup.html",context)
    #
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return redirect("index")
    #     else:
    #         context = {'ERROR': True}
    #         return render(request, "signup.html")
    # context = {}
    # return render(request, "signup.html", context)

def login(request):
    context = {'Title':TITLE}
    return render(request, "login.html", context)
