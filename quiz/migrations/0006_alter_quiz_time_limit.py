# Generated by Django 5.2.1 on 2025-06-06 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_rename_correctanswers_quizattempt_correct_answers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='time_limit',
            field=models.PositiveIntegerField(default=60),
        ),
    ]
