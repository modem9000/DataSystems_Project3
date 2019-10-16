"""
Definition of models.
"""

from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save



class Poll(models.Model):
    """A poll object for use in the application views and repository."""
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    author = models.CharField(max_length=100, blank=True)

    def total_votes(self):
        """Calculates the total number of votes for this poll."""
        return self.choice_set.aggregate(Sum('votes'))['votes__sum']

    def __unicode__(self):
        """Returns a string representation of a poll."""
        return self.text

class Choice(models.Model):
    """A poll choice object for use in the application views and repository."""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def votes_percentage(self):
        """Calculates the percentage of votes for this choice."""
        total=self.poll.total_votes()
        return self.votes / float(total) * 100 if total > 0 else 0

    def __unicode__(self):
        """Returns a string representation of a choice."""
        return self.text

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=26, default='')
    last_name = models.CharField(max_length=26, default='')
    email = models.CharField(max_length=50, default='')
    creation_date = models.DateTimeField(default=timezone.now)

    def create(self):
        self.creation_date = timezone.now
        self.save

    def  __str__(self):
        return self.first_name

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=26, default='')
    last_name = models.CharField(max_length=26, default='')
    email = models.EmailField(max_length=100, default='')
    creation_date = models.DateTimeField(default=timezone.now)

    def create(self):
        self.creation_date = timezone.now
        self.save

    def  __str__(self):
        return self.first_name

class Session(models.Model):
    tutor = models.ManyToManyField(User)
    student = models.ManyToManyField(Student)
    session_choice = (
        ('I', 'Individual'),
        ('G', 'Group'),
    )
    date = models.DateTimeField(default = timezone.now)
    size = models.IntegerField(default = 1)

    

class Quiz(models.Model):
    Session = models.ManyToManyField(Session)
    name = models.CharField(max_length=26, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=timezone.now)


class Question(models.Model):
    quiz = models.ManyToManyField(Quiz)
    question = models.TextField()


class Answer(models.Model):
    answer = models.CharField(max_length=200, default='')
    correct = models.BooleanField(default=False)
    question = models.ManyToManyField(Question)

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Tutor.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)