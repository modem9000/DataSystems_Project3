# Generated by Django 2.2.5 on 2019-10-16 05:34

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_answer_question_quiz_student_tutor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='question',
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ManyToManyField(to='app.Question'),
        ),
        migrations.RemoveField(
            model_name='question',
            name='quiz',
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ManyToManyField(to='app.Quiz'),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='email',
            field=models.EmailField(default='', max_length=100),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('size', models.IntegerField(default=1)),
                ('student', models.ManyToManyField(to='app.Student')),
                ('tutor', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='quiz',
            name='Session',
            field=models.ManyToManyField(to='app.Session'),
        ),
    ]