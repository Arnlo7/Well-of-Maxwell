from dataclasses import fields
from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from well_of_maxwell.models import *

'''
Models.py: Allows declaration of django forms, which can be instantiated by views.py
and saved into the SQLite databse. Can be used to easily update values in the
controller and provides a bridge between user input and database content.
'''
class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ('page_title', 'page_image', 'difficulty')
        widgets = {
            'page_title': forms.Textarea(attrs = {'rows': '1', 'id':'id_page_title_input_text'}),
            'page_image': forms.FileInput(attrs = {'id':'id_page_image'}),
            'difficulty': forms.NumberInput(attrs={'class': 'form-control'})
        }
        labels = {
            'page_title': "Page Title",
            'page_image': "Page Image",
            'difficulty': "Difficulty"
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)
        widgets = {
            'image': forms.FileInput(attrs = {'id':'id_image'})
        }
        labels = {
            'image': "Image"
        }

class QuizForm(forms.Form):
    question = forms.CharField(max_length = 300)
    answer_choices = forms.CharField(max_length=2000)
    correct = forms.CharField(max_length = 300)
    number = forms.CharField(max_length = 300)

class ExerciseForm(forms.Form):
    question = forms.CharField(max_length = 300)
    answer_choices = forms.CharField(max_length=2000)
    correct = forms.CharField(max_length = 300)
    '''
    def clean_answers(self):
        answers = self.cleaned_data.get('answer_choices')
        no_whitespace_answers = "".join(answers.split())
        answer_list = no_whitespace_answers.split(',')
        object_list = []
        for item in answer_list:
            if not Answer.objects.filter(text = item):
                new_answer = Answer(text = item)
                new_answer.save()
                object_list.append(new_answer)
            else:
                new_answer = Answer.objects.filter(text = item)[0]
                object_list.append(new_answer)
        return object_list
    '''

