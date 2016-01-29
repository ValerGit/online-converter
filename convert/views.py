from django.shortcuts import render
from converter.tasks import convert_to_mongo



def proceed_convert(request):
    data = {
        'from': {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '123456',
            'db': 'askdb',
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
                'name': 'ask_question',
                'isEmbedded': False
            },
            {
                'name': 'ask_answer',
                'isEmbedded': True,
                'embeddedIn': 'ask_question',
                'selfKey': 'question_id',
                'parentKey': 'id'
            }
        ]
    }
    result = convert_to_mongo.delay(data)
    return render(request, 'convertation.html', {'task_id': result.task_id})


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
