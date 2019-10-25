"""
Definition of urls for DjangoPolls.
"""

from datetime import datetime
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from app.views import CreateQuiz, CreateQuestions, CreateSession, TutorSignUp, StudentSignUp

urlpatterns = [
    path('', include(('app.urls', "app"), "appurls")),
    path('contact', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('seed/', views.seed, name='seed'),
    path('login/', 
        LoginView.as_view
        (
            template_name='app/login.html', 
            authentication_form=forms.BootstrapAuthenticationForm,
            extra_context =
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
         ),
        name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('setquiz/', CreateQuiz.as_view(), name='setquiz'),
    path('questions/', CreateQuestions.as_view(), name='setquestion'),
    path('sessions/', CreateSession.as_view(), name='setsession'),
    path('tutorhome/', views.tutorhome, name='tutorhome'),
    path('studenthome/', views.studenthome, name='studenthome'),
    path('signup/', views.signup, name='signup'),
    path('tutorsignup/', TutorSignUp.as_view(), name='tutorsignup'),
    path('studentsignup/', StudentSignUp.as_view(), name='studentsignup'),

]
