# Generated by Django 2.2.5 on 2019-10-17 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_question_quiz_session_student_tutor'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='session_choice',
            field=models.CharField(choices=[('I', 'Individual'), ('G', 'Group')], default='individual', max_length=2),
        ),
    ]
