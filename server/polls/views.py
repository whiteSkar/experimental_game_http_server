from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import Question


def index(request):
    recent_questions = Question.objects.order_by('-date_published')[:5]
    context = {
        'recent_questions': recent_questions,
    }

    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question %s does not exist" % question_id)

    context = {
        'question': question,
    }

    return render(request, 'polls/detail.html', context)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
