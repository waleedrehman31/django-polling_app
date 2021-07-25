from django.db.models.query import RawQuerySet
from django.template import loader
from django.urls import reverse
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Questions, Choice

# Create your views here.

# Get question and display them


def index(request):
    latest_question_list = Questions.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list
    }
    return render(request, 'polls/index.html', context)


# Show specific question and choices
def detail(request, question_id):
    try:
        question = Questions.objects.get(pk=question_id)
    except Questions.DoesNotExist:
        raise Http404('Question Does Not Exist')
    return render(request, 'polls/detail.html', {'question': question})


# Get question and display result
def results(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


# vote for a question choice
def vote(request, question_id):
    # print(request.POST['choice'])
    question = get_object_or_404(Questions, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You don\'t select a choice'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
