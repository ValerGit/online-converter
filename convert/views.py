from django.shortcuts import render
from converter.tasks import debug_task


def proceed_convert(request):
    result = debug_task.delay()
    return render(request, 'convertation.html', {'task_id': result.task_id})