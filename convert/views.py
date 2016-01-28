from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'base.html')


def signin(request):
    return render(request, 'signin.html')


def signup(request):
    return render(request, 'signup.html')


def account(request):
    return render(request, 'account.html')


def graphs(request):
    return render(request, 'graphs.html')


def ports(request):
    return render(request, 'choose_db.html')


def tables(request):
    return render(request, 'convertation.html')
