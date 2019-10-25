"""
Definition of views.
"""

import json
from os import path
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView, TemplateView
from app.models import Choice, Poll, Session, Quiz, Question
from django.contrib.auth.forms import UserCreationForm
from app.forms import RegistrationForm, CreateQuizForm, CreateQuestionForm, CreateSessionForm#, TutorSignUpForm, StudentSignUpForm

class PollListView(ListView):
    """Renders the home page, with a list of all polls."""
    model = Poll

    def get_context_data(self, **kwargs):
        context = super(PollListView, self).get_context_data(**kwargs)
        context['title'] = 'Polls'
        context['year'] = datetime.now().year
        return context

class PollDetailView(DetailView):
    """Renders the poll details page."""
    model = Poll

    def get_context_data(self, **kwargs):
        context = super(PollDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Poll'
        context['year'] = datetime.now().year
        return context

class PollResultsView(DetailView):
    """Renders the results page."""
    model = Poll

    def get_context_data(self, **kwargs):
        context = super(PollResultsView, self).get_context_data(**kwargs)
        context['title'] = 'Results'
        context['year'] = datetime.now().year
        return context

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def vote(request, poll_id):
    """Handles voting. Validates input and updates the repository."""
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'app/details.html', {
            'title': 'Poll',
            'year': datetime.now().year,
            'poll': poll,
            'error_message': "Please make a selection.",
    })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('app:results', args=(poll.id,)))

@login_required
def seed(request):
    """Seeds the database with sample polls."""
    samples_path = path.join(path.dirname(__file__), 'samples.json')
    with open(samples_path, 'r') as samples_file:
        samples_polls = json.load(samples_file)

    for sample_poll in samples_polls:
        poll = Poll()
        poll.text = sample_poll['text']
        poll.pub_date = timezone.now()
        poll.save()

        for sample_choice in sample_poll['choices']:
            choice = Choice()
            choice.poll = poll
            choice.text = sample_choice
            choice.votes = 0
            choice.save()

    return HttpResponseRedirect(reverse('app:home'))

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            args = {
                'title':'Sign Up Selection',
                'year':datetime.now().year,
                }
            return render(request, app/about.html, args)
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'app/register.html', args)

def signup(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/signuplayout.html',
        {
            'title':'Sign Up Selection',
            'year':datetime.now().year,
        }
    )

class TutorSignUp(TemplateView):
    template_name = 'app/register.html'

    def get(self, request):
        form = TutorSignUpForm()
        return render(request, self.template_name, {
            'form': form,
            'title': 'Select Classes',
            })

    def post(self, request):
        form = TutorSignUpForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('/setquiz')

        args = {'form': form,}
        return render(request, self.template_name, args)

class StudentSignUp(TemplateView):
    template_name = 'app/register.html'

    def get(self, request):
        form = StudentSignUpForm()
        return render(request, self.template_name, {
            'form': form,
            'title': 'Select ',
            })

    def post(self, request):
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('/studenthome')

        args = {'form': form,}
        return render(request, self.template_name, args)

@login_required
def tutorhome(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/tutorlayout.html',
        {
            'title':'Tutor Home Page',
            'year':datetime.now().year,
        }
    )

@login_required
def studenthome(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/studentlayout.html',
        {
            'title':'Student Home Page',
            'year':datetime.now().year,
        }
    )

class CreateSession(TemplateView):
    template_name = 'app/tutor.html'

    @login_required
    def get(self, request):
        form = CreateSessionForm()
        return render(request, self.template_name, {
            'form': form,
            'title': 'Create Session',
            })

    @login_required
    def post(self, request):
        form = CreateSessionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('/setquiz')

        args = {'form': form,}
        return render(request, self.template_name, args)

class CreateQuiz(TemplateView):
    template_name = 'app/tutor.html'

    @login_required
    def get(self, request):
        form = CreateQuizForm()
        sessions = Session.objects.all()
        return render(request, self.template_name, {
            'form': form,
            'title': 'Create Quiz',
            })

    @login_required
    def post(self, request):
        form = CreateQuizForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('/questions')

        args = {'form': form,}
        return render(request, self.template_name, args)

class CreateQuestions(TemplateView):
    template_name = 'app/tutor.html'

    @login_required
    def get(self, request):
        form = CreateQuestionForm
        return render(request, self.template_name, {'form': form})

    @login_required
    def post(self, request):
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('/answers')

        args = {'form': form,}
        return render(request, self.template_name, args)
            