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
from convert import utils
from convert.models import Database, ConvertedDatabase
import datetime


def proceed_convert(request):
    if request.is_ajax():
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
            except ValueError:
                return HttpResponseBadRequest()
            try:
                from_database = Database.objects.get(id=data['from'], user=request.user)
                to_database = Database.objects.get(id=data['to'], user=request.user)
            except (Database.DoesNotExist, KeyError):
                return JsonResponse({'status': 'bad'})
            to_celery = {
                'from': {
                    'host': from_database.db_address,
                    'user': from_database.db_user,
                    'password': from_database.db_password,
                    'db': from_database.db_name
                },
                'to': {
                    'host': to_database.db_address,
                    'user': to_database.db_user,
                    'password': to_database.db_password,
                    'db': to_database.db_name
                },
                'tables': data['tables']
            }
            #  many many checks required !!!
            for table in data['tables']:
                if table['isEmbedded']:
                    exist = False
                    for t in data['tables']:
                        if table['embeddedIn'] == t['name']:
                            exist = True
                            break
                    if not exist:
                        to_celery['tables'].append({
                            'name': table['embeddedIn'],
                            'isEmbedded': False
                        })
            result = convert_to_mongo.delay(to_celery)
            conv_db = ConvertedDatabase()
            conv_db.database_from = from_database
            conv_db.database_to = to_database
            conv_db.user = request.user
            conv_db.celery_id = result.task_id
            conv_db.save()
            return JsonResponse({'status': 'ok', 'id': conv_db.id})

        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
    # data = {
    #     'from': {
    #         'host': '127.0.0.1',
    #         'user': 'root',
    #         'password': '',
    #         'db': 'galkin',
    #         'type': 'MY'
    #     },
    #     'to': {
    #         'host': '127.0.0.1',
    #         'user': '',
    #         'password': '',
    #         'db': 'forums',
    #         'type': 'MO'
    #     },
    #     'tables': [
    #         {
    #             'name': 'questions',
    #             'isEmbedded': False
    #         },
    #         {
    #             'name': 'answers',
    #             'isEmbedded': True,
    #             'embeddedIn': 'questions',
    #             'selfKey': 'id_Question',
    #             'parentKey': 'id'
    #         }
    #     ]
    # }
    # result = convert_to_mongo.delay(data)
    #return render(request, 'celery.html', {'task_id': result.task_id})


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
                return HttpResponseRedirect('/account/')
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


@login_required
def account(request):
    all_converted = ConvertedDatabase.objects.filter(user=request.user).order_by('-date')
    need_new_db = 0
    if not all_converted:
        need_new_db = 1
    return render(request, 'account.html', {'need_new_db': need_new_db, 'all_converted': all_converted,
                                            })


def graphs(request):
    return render(request, 'graphs.html')


def ports(request):
    return render(request, 'choose_db.html')


def tables(request):
    from_db = int(request.REQUEST.get('from'))
    to_db = int(request.REQUEST.get('to'))
    need_db_choose = 0
    if not from_db or not to_db:
        need_db_choose = 1
        all_mysqls = Database.objects.filter(type="MY", user=request.user)
        all_mongos = Database.objects.filter(type="MO", user=request.user)
        return render(request, 'convertation.html', {'need_db_choose': need_db_choose, 'all_mysql': all_mysqls,
                                                     'all_mongos': all_mongos})

    try:
        from_database = Database.objects.get(id=from_db, user=request.user)
        to_database = Database.objects.get(id=to_db, user=request.user)
    except Database.DoesNotExist:
        return HttpResponseRedirect('/tables-choose')
    return render(request, 'convertation.html', {
        'need_db_choose': need_db_choose,
        'from_db': from_db,
        'to_db': to_db
    })


@login_required
def check_status(request):
    if request.is_ajax():
        if request.method == 'GET':
            try:
                converting_database = ConvertedDatabase.objects.get(id=request.GET.get('id'), user=request.user)
            except ConvertedDatabase.DoesNotExist:
                return JsonResponse({'error': 'Конвертация не найдена, обратитесь в службу поддержки'})
            result = AsyncResult(converting_database.celery_id)
            current_progress = ''
            if result.status == 'PROGRESS':
                current_progress = result.result
            return JsonResponse(
                {
                    'status': result.status,
                    'ready': result.ready(),
                    'progress': current_progress
                }
            )
        else:
            return JsonResponse({'error': 'Неверный запрос'})
    else:
        return HttpResponseBadRequest()


@login_required
def create_db(request):
    if request.is_ajax():
        if request.method == "POST":
            try:
                data = json.loads(request.body)
            except ValueError:
                return HttpResponseBadRequest()
            try:
                for el in data['from']:
                    if not el:
                        return JsonResponse({'valid': 'no'})
                for el in data['to']:
                    if not el:
                        return JsonResponse({'valid': 'no'})
            except KeyError:
                return HttpResponseBadRequest()
            db_from = Database(user=request.user, **data['from'])
            db_from.save()
            db_to = Database(user=request.user, **data['to'])
            db_to.save()
            return JsonResponse({'valid': 'ok', 'from_id': db_from.id, 'to_id': db_to.id})
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


@login_required
def get_tables_by_db(request):
    if request.is_ajax():
        if request.method == "GET":
            db_id = request.GET.get('db_id')
            if db_id is None:
                return HttpResponseBadRequest()
            try:
                db = Database.objects.get(id=db_id)
            except Database.DoesNotExist:
                return JsonResponse({'status': 'bad'})
            if db.user != request.user:
                return JsonResponse({'status': 'bad'})
            conn = utils.check_mysql_connection(db.db_address, db.db_user, db.db_password, db.db_name)
            if not conn:
                return JsonResponse({'status': 'bad'})
            table_names = utils.get_table_names_by_connection(conn)
            return JsonResponse({'status': 'ok', 'tables': table_names})
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


@login_required
def get_attrs_by_table(request):
    if request.is_ajax():
        if request.method == "GET":
            db_id = request.GET.get('db_id')
            table_name = request.GET.get('table')
            if db_id is None or table_name is None:
                return HttpResponseBadRequest()
            try:
                db = Database.objects.get(id=db_id, user=request.user)
            except Database.DoesNotExist:
                return JsonResponse({'status': 'bad'})
            conn = utils.check_mysql_connection(db.db_address, db.db_user, db.db_password, db.db_name)
            if not conn:
                return JsonResponse({'status': 'bad'})
            attrs = utils.get_attrs_by_table(conn, table_name)
            return JsonResponse({'status': 'ok', 'attrs': attrs})
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


@login_required
def progress(request):
    # checks required
    id = int(request.GET.get('id'))
    if id is None:
        return HttpResponseBadRequest()
    try:
        conv = ConvertedDatabase.objects.get(id=id, user=request.user)
    except ConvertedDatabase.DoesNotExist:
        return HttpResponseRedirect('/account/')
    return render(request, 'progress.html', {'conv_id': id,
                                             'from_name': conv.database_from.db_name,
                                             'to_name': conv.database_to.db_name})


@login_required
def remove(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except ValueError:
            return HttpResponseBadRequest()
        id = int(data['table'])
        table = Database.objects.filter(pk=id).update(is_deleted=1)
        return JsonResponse({'status': 'ok'})

    all_dbs = Database.objects.filter(user=request.user, is_deleted=0)
    return render(request, 'removal.html', {'all_dbs': all_dbs})


@login_required
def get_pulse(request):
    now = datetime.datetime.now()
    all_converted = ConvertedDatabase.objects.filter(user=request.user)
    cntr = ConvertedDatabase.objects.filter(user=request.user, date__range=('2013-01-01', now)).count()
    data = []
    year = now.year
    end_year = year
    month = now.month
    end = month + 1
    for x in range(1, 12, 1):
        start_date = str(year)+'-'+str(month)+'-01'
        end_date = str(end_year)+'-'+str(end)+'-01'
        cntr = ConvertedDatabase.objects.filter(user=request.user, date__range=(start_date, end_date)).count()
        temp = {
            'date': start_date,
            'num': cntr,
        }
        data.append(temp)
        end = month
        month -= 1
        if month == 0:
            month = 12
            end_year = year
            year -= 1
            end = 1

        elif month == 11:
            end = 12
            end_year = year

    return JsonResponse({'data': data})