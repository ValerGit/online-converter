from django.shortcuts import render
from converter.tasks import convert_to_mongo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from forms import RegistrationForm, UserForms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def proceed_convert(request):
    data = {
        'from': {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '',
            'db': 'galkin',
            'type': 'MY'
        },
        'to': {
            'host': '127.0.0.1',
            'user': '',
            'password': '',
            'db': 'forums',
            'type': 'MO'
        },
        'tables': [
            {
                'name': 'questions',
                'isEmbedded': False
            },
            {
                'name': 'answers',
                'isEmbedded': True,
                'embeddedIn': 'questions',
                'selfKey': 'id_Question',
                'parentKey': 'id'
            }
        ]
    }
    result = convert_to_mongo.delay(data)
    return render(request, 'celery.html', {'task_id': result.task_id})


def home(request):
    return render(request, 'base.html')


def signin(request):
    user = request.user
    value = request.REQUEST.get('next', '')
    if request.method == 'POST':
        form = UserForms(request.POST)
        if form.is_valid():
            form.username = request.POST['username']
            form.password = request.POST['password']
            user = authenticate(username=form.username, password=form.password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.POST.get('next', ''))
    else:
        form = UserForms()
    return render(request, 'signin.html', {'form': form})


def signup(request):
    user = None
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.username = request.POST['username']
            form.email = request.POST['email']
            form.password1 = request.POST['password1']
            form.password2 = request.POST['password2']
            form.save()
            user = authenticate(username=form.username, password=form.password1)
            if user is not None:
                login(request, user)
                return home(request)
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})



def account(request):
    return render(request, 'account.html')


def graphs(request):
    return render(request, 'graphs.html')


def ports(request):
    return render(request, 'choose_db.html')


def tables(request):
    return render(request, 'convertation.html')
