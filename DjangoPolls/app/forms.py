"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app.models import Quiz, Question, Session
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

#class TutorSignUpForm(forms.ModelForm):


#class StudentSignUpForm(forms.ModelForm):

class CreateSessionForm(forms.ModelForm):
   # session_type = forms.ChoiceField(choices = Session.session_choices)
   date = forms.DateTimeField()
   size = forms.IntegerField()
   class Meta:
       model = Session
       fields = ('session_choice',
                 'date',
                 'size',
                 )

class CreateQuizForm(forms.ModelForm):
    session = forms.ModelChoiceField(queryset=Session.objects.all())
    name = forms.CharField(max_length=26, required=True)
    creation_date = forms.DateTimeField()
    due_date = forms.DateTimeField()

    class Meta:
        model = Quiz
        fields = ('session',
                  'name',
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
                  'answer1',
                  'correct1',
                  'answer2',
                  'correct2',
                  'answer3',
                  'correct3',
                  'answer4',
                  'correct4'
                  )


