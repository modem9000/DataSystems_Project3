"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app.models import Quiz, Question, Answer
from django.utils import timezone

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

class CreateQuizForm(forms.ModelForm):
    name = forms.CharField(max_length=26, required=True)
    creation_date = forms.DateTimeField()
    due_date = forms.DateTimeField()

    class Meta:
        model = Quiz
        fields = ('name',
                  'creation_date',
                  'due_date'
                  )

class CreateQuestionForm(forms.ModelForm):
    quiz = forms.CharField(max_length=26, required=True)
    question = forms.CharField(max_length=26, required=True)
    answer = forms.CharField(max_length=26, required=True)

    class Meta:
        model = Question
        fields = ('quiz',
                  'question',
                  )

class CreateAnswerForm(forms.ModelForm):
    question = forms.CharField(max_length=26, required=True)
    answer = forms.CharField(max_length=26, required=True)
    correct = forms.BooleanField()

    class Meta:
        model = Answer
        fields = ('question',
                  'answer',
                  'correct'
                  )


