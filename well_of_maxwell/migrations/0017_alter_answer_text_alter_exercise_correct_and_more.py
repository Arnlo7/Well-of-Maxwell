# Generated by Django 4.2 on 2023-05-08 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('well_of_maxwell', '0016_remove_guest_experience_delete_leaderboard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='correct',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='question',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='correct',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='question',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='quizanswer',
            name='text',
            field=models.CharField(default='', max_length=300),
        ),
    ]