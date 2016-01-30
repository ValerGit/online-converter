# -*- coding: utf-8 -*-

from django.shortcuts import render
from converter.tasks import convert_to_mongo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from forms import RegistrationForm, UserForms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from forms import RegistrationForm
from celery.result import AsyncResult
from convert.models import ConvertedDatabase, Database
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import json
from convert.models import Database


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
    from_db = request.REQUEST.get('from')
    to_db = request.REQUEST.get('to')
    need_db_choose = 0
    if not from_db or not to_db:
        need_db_choose = 1
        all_mysqls = Database.objects.filter(type="MY")
        all_mongos = Database.objects.filter(type="MO")

    return render(request, 'convertation.html', {'need_db_choose': need_db_choose, 'all_mysql':all_mysqls,
                                                 'all_mongos':all_mongos})


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


@login_required
def create_db(request):
    if request.is_ajax():
        if request.method == "POST":
            data = json.loads(request.body)
            for el in data['from']:
                if not el:
                    return JsonResponse({'valid': 'no'})
            for el in data['to']:
                if not el:
                    return JsonResponse({'valid': 'no'})
            db_from = Database(user=request.user, **data['from'])
            db_from.save()
            db_to = Database(user=request.user, **data['to'])
            db_to.save()
            return JsonResponse({'valid': 'ok', 'from_id': db_from.id, 'to_id': db_to.id})
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

