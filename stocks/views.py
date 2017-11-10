from django.shortcuts import render

# Create your views here.

def index(request):
    context = {'Title':"Title"}
    return render(request, "index.html", context)

def signup(request):
    context = {'Title':"Title"}
    return render(request, "signup.html", context)

def login(request):
    context = {'Title':"Title"}
    return render(request, "login.html", context)
