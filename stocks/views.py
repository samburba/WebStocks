from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.

TITLE = "Title"

def index(request):
    context = {'Title':TITLE}
    return render(request, "index.html", context)

def signup(request):
    #  following the tutorial here: https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticcation(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    context = {'Title':TITLE, 'form':form}
    return render(request, "signup.html", context)

def login(request):
    context = {'Title':TITLE}
    return render(request, "login.html", context)
