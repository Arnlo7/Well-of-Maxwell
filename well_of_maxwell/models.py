from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

'''
Models.py: Allows declaration of models, which can be instantiated by views.py
and saved into the SQLite databse. This file determines the columns of the 
SQLite databse. 
'''

# Create your models here.
class Module(models.Model):
    page_title = models.CharField(max_length = 100)
    page_image = models.FileField(blank=False, default = '')
    module_type = models.IntegerField(default = 0)
    number = models.IntegerField(default = 0)
    difficulty = models.IntegerField(default = 0)

class Content(models.Model):
    section_title = models.CharField(max_length = 50)
    module = models.ForeignKey(Module,on_delete = models.PROTECT)

class Text(models.Model):
    text = models.CharField(max_length = 500, default = '')
    content_block = models.ForeignKey(Content, on_delete = models.PROTECT)

class Exercise(models.Model):
    correct = models.CharField(max_length = 300)
    question = models.CharField(max_length = 300, default = '')
    content_block = models.ForeignKey(Content, on_delete = models.PROTECT, default = None)

class Quiz(models.Model):
    correct = models.CharField(max_length = 300)
    question = models.CharField(max_length = 300, default = '')
    number = models.IntegerField(default = 0)
     
class Answer(models.Model):
    text = models.CharField(max_length = 300, default = '')
    exercise_block = models.ForeignKey(Exercise,on_delete = models.PROTECT, default = None)

class QuizAnswer(models.Model):
    text = models.CharField(max_length = 300, default = '')
    quiz_block = models.ForeignKey(Quiz,on_delete = models.PROTECT, default = None)

class Image(models.Model):
    image = models.FileField(blank=False)
    content_block = models.ForeignKey(Content, on_delete = models.PROTECT)

class Plot(models.Model):
    image = models.FileField(blank=False)

class Guest(models.Model):
    username = models.CharField(max_length = 20)


class Score(models.Model):
    username = models.CharField(max_length = 20)
    score = models.IntegerField()


