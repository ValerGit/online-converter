# -*- coding: utf-8 -*-

from django.shortcuts import render
from converter.tasks import convert_to_mongo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from forms import RegistrationForm
from celery.result import AsyncResult
from convert.models import ConvertedDatabase
from django.http import JsonResponse
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
    return render(request, 'signin.html')


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


@login_required
def check_status(request):
    if request.method == 'GET':
        try:
            converting_database = ConvertedDatabase.objects.get(id=request.GET.get('id'))
        except ConvertedDatabase.DoesNotExist:
            return JsonResponse({'error': 'Конвертация не найдена, обратитесь в службу поддержки'})
        if converting_database.user != request.user:
            return JsonResponse({'error': 'Конвертация не найдена, обратитесь в службу поддержки'})
        result = AsyncResult(converting_database.celery_id)
        return JsonResponse(
            {
                'status': result.status,
                'ready': result.ready()
            }
        )
    else:
        return JsonResponse({'error': 'Неверный запрос'})
