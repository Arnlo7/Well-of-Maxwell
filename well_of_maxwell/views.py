from django.shortcuts import render
from http.client import HTTPResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.db.models import Q

from well_of_maxwell.models import *
from well_of_maxwell.forms import *
import json

import csv
import libm2k
import matplotlib.pyplot as plt
import time
import numpy as np
import csv
from scipy.signal import butter,filtfilt

'''
Views.py: Functions as the main controller file for the web application. Many 
functions to recieve HTTP requests as well as XML requests, and can context 
variables sent to views and create new model instances. 
'''
'''Some code seen here may be adapted from 17-437 Web application development at Carnegie Mellon University'''
'''HELPER FUNCTIONS
##################################################################################################################################

##################################################################################################################################
'''
#initial_context: None -> dict: Base Function to return a dummy context dictionary. 
def initial_context():
    return {}

#is_admin: request -> bool: checks whether the user in the current request is an administrator
def is_admin(request):
    if request.user.is_anonymous:
        return False
    if (request.user.email.startswith("shizhenl") or 
        request.user.email.startswith("muditm") or
        request.user.email.startswith("aqlao")):
        return True

'''
login_complete_action: request-> web page: immediately called after OAuth return
and directs to admin page or welcome page based on login. 
'''
def login_complete_action(request):
    if is_admin(request):
        return redirect("admin")
    else:
        return redirect("welcome")
'''
set_module_context: (request,int)-> dict: helper function that given an module 
ID, returns the page title and module number.
'''
def set_module_context(request,id):
    module = Module.objects.get(id=id)
    context = {}
    context['page_title'] = module.page_title
    context['module_id'] = module.id
    return context

'''ACTION FUNCTIONS: called by urls.py, render views to web application
##################################################################################################################################

##################################################################################################################################
'''
#welcome_action: request -> web page: renders welcome.html with no context
def welcome_action(request):
    if request.method == 'GET':
        context = initial_context()
        return render(request, 'well_of_maxwell/welcome.html', context)

'''
difficulty_action: request -> web page: creates guest username based on input 
and renders difficulty.html
'''
def difficulty_action(request):
    if request.method == "POST":
        username = request.POST['username-text']
        for temp in Guest.objects.all():
            temp.delete()
        curr_guest = Guest()
        curr_guest.username = username
        curr_guest.save()
        context = {}
        context["Guest"] = curr_guest
        return render(request, 'well_of_maxwell/difficulty.html', context)
    if request.method == 'GET':
        context = initial_context()
        return render(request, 'well_of_maxwell/difficulty.html', context)

'''home_action: (request,int,int)-> web page: shows module content and generates
context variables for the corresponding module page (based on id, and difficulty).
This function is only applicable to module_type==0, which corresponds to non experiment
modules. '''
def home_action(request, id, difficulty):
    #Takes count of number of non experiment modules in this difficulty bracket
    length_check = 0
    for module in Module.objects.all():
        if module.module_type == 0 and module.difficulty == difficulty:
            length_check+=1
    module = Module.objects.get(id=id)
    curr_number = module.number
    next_number = curr_number+1
    prev_number = curr_number-1
    #Finds the ID of the modules to display for "next" and "previous" buttons
    prev_id = 0
    next_id = 0
    for temp in Module.objects.all():
        if temp.number == next_number and temp.module_type == 0 and temp.difficulty == module.difficulty:
            next_id = temp.id
        if temp.number == prev_number and temp.module_type == 0 and temp.difficulty == module.difficulty:
            prev_id = temp.id
    '''
    Generates context variables, grabbing all content blocks associated with the
    module, text within these content blocks, images within these content blocks,
    exercises within these content blocks, and answers corresponding to the 
    exercises and returns them as context variables for display on the HTMl page.
    '''
    contents = set()
    texts = set()
    images = set()
    exercises = set()
    answers = set()
    for content in Content.objects.all():
        if content.module.id == module.id:
            curr_content = content
            contents.add(curr_content)
    #Break to avoid adding duplicates of text
    for text in Text.objects.all():
        curr_text_added = False
        for content in contents:
            if text.content_block.id == content.id:
                texts.add(text)
                curr_text_added = True
                break
        if(curr_text_added):
            continue      
    for image in Image.objects.all():
        curr_image_added = False
        for content in contents:
            if image.content_block.id ==content.id:
                images.add(image)
                curr_image_added = True
                break
        if(curr_image_added):
            continue
    for exercise in Exercise.objects.all():
        curr_exercise_added = False
        for content in contents:
            if exercise.content_block.id ==content.id:
                exercises.add(exercise)
                curr_exercise_added = True
                break
        if(curr_exercise_added):
            continue
    for answer in Answer.objects.all():
        for exercise in exercises:
            if answer.exercise_block.id == exercise.id and exercise.content_block.id == content.id:
                answers.add(answer)
    '''
    To avoid the experiment hub, finds the ID of the first experiment module
    for each experiment and returns as a context variable.
    '''
    lowest = 999
    lowest_exp1 = 0
    for curr in Module.objects.all():
        if(curr.module_type==1):
            if(curr.number<lowest):
                lowest = curr.number
                lowest_exp1 = curr.id
    lowest = 999
    lowest_exp2 = 0
    for curr in Module.objects.all():
        if(curr.module_type==2):
            if(curr.number<lowest):
                lowest = curr.number
                lowest_exp2 = curr.id
    context = {'exp2_id': lowest_exp2,'exp1_id': lowest_exp1,'module': module, 'text': texts, 'image':images, 'answer':answers,'exercise':exercises, 'content': contents, 'max_length': length_check, 'next_id': next_id, 'prev_id': prev_id, 'form':ImageForm(), 'form2':ExerciseForm(), 'difficulty':difficulty}
    if (is_admin(request)):
        context['isAdmin'] = True
    else:
        context['isAdmin'] = False
    if (request.method == "GET"):
        return render(request, 'well_of_maxwell/home.html', context)

'''hub_action: request-> web page: renders the hub web page, returning all
existing module objects as context variables. Further filtered in HTML page.'''
def hub_action(request):
    if (request.method == "GET"):
        modules = set()
        difficulty = set()
        for module in Module.objects.all():
            difficulty.add(module.difficulty)
            modules.add(module)
        return render(request,'well_of_maxwell/hub.html', {'modules':modules, 'difficulty':difficulty})

'''home_hub_action: request-> web page: returns all modules of a specific 
difficulty level instead of all existing. Very similar to above function.'''
def home_hub_action(request,difficulty):
    if (request.method =="GET"):
        modules = set()
        for module in Module.objects.all():
            if(module.difficulty == difficulty):
                modules.add(module)
        return render(request,'well_of_maxwell/home-hub.html', {'modules':modules, 'difficulty':difficulty})
    
'''exp1_hub_action: request-> web page: returns all experiment 1 modules.'''
def exp1_hub_action(request):
    if (request.method =="GET"):
        modules = set()
        for module in Module.objects.all():
            modules.add(module)
        return render(request,'well_of_maxwell/exp1_hub.html', {'modules':modules})
    
'''exp2_hub_action: request-> web page: returns all experiment 2 modules.'''
def exp2_hub_action(request):
    if (request.method =="GET"):
        modules = set()
        for module in Module.objects.all():
            modules.add(module)
        return render(request,'well_of_maxwell/exp2_hub.html', {'modules':modules})

'''admin_action: request-> web page: renders admin page, called when clicking on admin link'''
@login_required
def admin_action(request):
    context = initial_context()
    return render(request, 'well_of_maxwell/admin.html', context)

'''exp1_action: (request, int, int)-> web page: very similar to home_action, but returns
experiment 1 modules instead of non experimental modules.'''
def exp1_action(request, id,difficulty):
    length_check = 0
    L = []
    for module in Module.objects.all():
        if module.module_type == 1:
            length_check+=1
            L.append(module)
    module = Module.objects.get(id=id)
    curr_number = module.number
    next_number = curr_number+1
    prev_number = curr_number-1
    prev_id = 0
    next_id = 0
    for temp in Module.objects.all():
        if temp.number == next_number and temp.module_type == 1 and temp.difficulty == module.difficulty:
            next_id = temp.id
        if temp.number == prev_number and temp.module_type == 1 and temp.difficulty == module.difficulty:
            prev_id = temp.id
    contents = set()
    texts = set()
    images = set()
    exercises = set()
    for content in Content.objects.all():
        if content.module.id == module.id:
            curr_content = content
            contents.add(curr_content)
    for text in Text.objects.all():
        curr_text_added = False
        for content in contents:
            if text.content_block.id == content.id:
                texts.add(text)
                curr_text_added = True
                break
        if(curr_text_added):
            continue      
    for image in Image.objects.all():
        curr_image_added = False
        for content in contents:
            if image.content_block.id ==content.id:
                images.add(image)
                curr_image_added = True
                break
        if(curr_image_added):
            continue
    for exercise in Exercise.objects.all():
        curr_exercise_added = False
        for content in contents:
            if exercise.content_block.id ==content.id:
                exercises.add(exercise)
                curr_exercise_added = True
                break
        if(curr_exercise_added):
            continue
    context = {'module': module, 'text': texts, 'image':images, 'exercise':exercises, 'content': contents, 'max_length': length_check, 'next_id': next_id, 'prev_id': prev_id, 'form':ImageForm(), 'form2':ExerciseForm()}
    if (is_admin(request)):
        context['isAdmin'] = True
    else:
        context['isAdmin'] = False
    if (request.method == "GET"):
        return render(request, 'well_of_maxwell/exp1.html', context)

'''exp1_end_action: request-> web page: renders Faraday's Experiment page'''
def exp1_end_action(request):
    context=initial_context()
    if (request.method == "GET"):
        return render(request, 'well_of_maxwell/exp1_end.html', context)

'''exp2_action: (request, int, int)-> web page: very similar to home_action, but returns
experiment 2 modules instead of non experimental modules.'''
def exp2_action(request, id, difficulty):
    length_check = 0
    L = []
    for module in Module.objects.all():
        if module.module_type == 2:
            length_check+=1
            L.append(module)
    module = Module.objects.get(id=id)
    curr_number = module.number
    next_number = curr_number+1
    prev_number = curr_number-1
    prev_id = 0
    next_id = 0
    for temp in Module.objects.all():
        if temp.number == next_number and temp.module_type == 2 and temp.difficulty == module.difficulty:
            next_id = temp.id
        if temp.number == prev_number and temp.module_type == 2 and temp.difficulty == module.difficulty:
            prev_id = temp.id
    contents = set()
    texts = set()
    images = set()
    exercises = set()
    for content in Content.objects.all():
        if content.module.id == module.id:
            curr_content = content
            contents.add(curr_content)
    for text in Text.objects.all():
        curr_text_added = False
        for content in contents:
            if text.content_block.id == content.id:
                texts.add(text)
                curr_text_added = True
                break
        if(curr_text_added):
            continue      
    for image in Image.objects.all():
        curr_image_added = False
        for content in contents:
            if image.content_block.id ==content.id:
                images.add(image)
                curr_image_added = True
                break
        if(curr_image_added):
            continue
    for exercise in Exercise.objects.all():
        curr_exercise_added = False
        for content in contents:
            if exercise.content_block.id ==content.id:
                exercises.add(exercise)
                curr_exercise_added = True
                break
        if(curr_exercise_added):
            continue
    context = {'module': module, 'text': texts, 'image':images, 'exercise':exercises, 'content': contents, 'max_length': length_check, 'next_id': next_id, 'prev_id': prev_id, 'form':ImageForm(), 'form2':ExerciseForm()}
    if (is_admin(request)):
        context['isAdmin'] = True
    else:
        context['isAdmin'] = False
    if (request.method == "GET"):
        return render(request, 'well_of_maxwell/exp2.html', context)
    
'''exp2_end_action: request-> web page: renders Faraday's Experiment page'''
def exp2_end_action(request):
    context=initial_context()
    if (request.method == "GET"):
        return render(request, 'well_of_maxwell/exp2_end.html', context)
    
'''quiz_start_action: request-> web page: renders quiz introduction page'''
def quiz_start_action(request):
    context = initial_context()
    return render(request, "well_of_maxwell/quiz_start.html",context)

'''reset_quiz: request-> web page: helper function that finds name of current guest
for placement on leaderboard, and creates score instance. Then directs to first
question of the quiz'''
def reset_quiz_action(request):
    curr_guest = Guest.objects.all()[0]
    new_score = Score()
    new_score.score = 0
    new_score.username = curr_guest.username
    new_score.save()
    return quiz_action(request,1,new_score.id)

'''parse_quiz: (request, int, int, int) -> web page: determines how many points
to add to the current score, and loads next question'''
def parse_quiz(request, number, score_id,correct):
    #answered correctly
    if (correct == 0):
        curr_score = Score.objects.get(id=score_id)
        temp = curr_score.score
        temp = temp + 100
        curr_score.score = temp
        curr_score.save()
    else:
        curr_score = Score.objects.get(id=score_id)
        temp = curr_score.score
        temp = temp + 50
        curr_score.score = temp
        curr_score.save()
    #answered incorrectly
    return quiz_action(request,number,score_id)

'''quiz_action: (request, int, int): renders leaderoard, as well as loads
context for the current quiz question.'''
def quiz_action(request,number,score_id):
    length_check = 0
    for quiz in Quiz.objects.all():
        length_check+=1
    context = {}
    if (number>length_check or number == 0):
        score_copy = []
        for score in Score.objects.all():
            score_copy.append(score)
        scores = []
        temp = []
        for score in Score.objects.all():
            temp.append(score.score)
        temp.sort()
        temp.reverse()

        for item in temp:
            for score in score_copy:
                if (score.score == item):
                    scores.append(score)
                    score_copy.remove(score)
                    break
        context["scores"] = scores
        return render(request, 'well_of_maxwell/leaderboard.html',context)
    quiz = Quiz.objects.get(number=number)
    curr_number = quiz.number
    next_number = curr_number+1
    next_id = 0
    for temp in Quiz.objects.all():
        if temp.number == next_number:
            next_id = temp.id
    quizzes = set()
    quizzes.add(quiz)
    answers = set()
    for answer in QuizAnswer.objects.all():
        for curr_quiz in quizzes:
            if answer.quiz_block.id == curr_quiz.id:
                answers.add(answer)
    context = {'answers':answers,'quizzes':quizzes,'next_id': next_id,'score_id':score_id}
    if (request.method == "GET"):
        return render(request, 'well_of_maxwell/quiz.html',context)

'''edit_home_action: request-> web page: renders edit_home page, and returns form
for uploading new modules. Django form, referenced in forms.py'''
def edit_home_action(request):
    if (request.method == "GET"):
        context = {'form':ModuleForm(),
                   }
        return render(request, 'well_of_maxwell/edit_home.html',context)

'''add_image_action: (request,int, int, int)-> web page: function for processing
photos uploaded to module pages. Creates a new image model, and saves it to the
corresponding context block. Then redirects back to previous page'''
def add_image_action(request,content_id,home_id,difficulty):
    if (request.method == "POST"):
        form = ImageForm(request.POST,request.FILES)
        if not form.is_valid():
            context = {'form':form}
            return render(request,'well_of_maxwell/home.html',context)
        image = form.cleaned_data['image']
        content_block = Content.objects.get(id=content_id)
        new_image = Image()
        new_image.image = image
        new_image.content_block = content_block
        new_image.save()
        context = initial_context()
        return redirect("home",home_id,difficulty)

'''add_exercise_action: (request,int, int, int)-> web page: function for processing
exercises uploaded to module pages. Creates a new exercise model, and saves it to the
corresponding context block. Then redirects back to previous page'''
def add_exercise_action(request,content_id,home_id,difficulty):
    if (request.method == "POST"):
        form = ExerciseForm(request.POST)
        if not form.is_valid():
            context = {'form':form}
            return render(request,'well_of_maxwell/home.html',context)
        new_exercise = Exercise(question = form.cleaned_data['question'])
        new_exercise.content_block = Content.objects.get(id=content_id)
        new_exercise.save()
        #adding the answer objects
        answers = form.cleaned_data.get('answer_choices')
        temp_answer_list = answers.split(',')
        answer_list = []
        for item in temp_answer_list:
            stripped = item.strip()
            answer_list.append(stripped)
        answer_choices = []
        for item in answer_list:
            new_answer = Answer(text = item)
            new_answer.exercise_block = new_exercise
            new_answer.save()
            answer_choices.append(new_answer)
        check = False
        for answer in answer_choices:
            if (check):
                break
            if answer.text == form.cleaned_data['correct']:
                target = answer
                check = True
        new_exercise.correct = target.text
        new_exercise.save()
        return redirect("home",home_id,difficulty)

'''get_module_photo: (request, int) -> web page: fetches image data from the database'''
def get_module_photo(request,id):
    item = get_object_or_404(Module,id=id)
    print('Picture #{} fetched from db: {} (type={})'.format(id, item.page_image, type(item.page_image)))
    if not item.page_image:
        raise Http404
    return HttpResponse(item.page_image)

'''get_content_photo: (request, int) -> web page: fetches image data from the database'''
def get_content_photo(request,id):
    item = get_object_or_404(Image, id=id)
    print('Picture #{} fetched from db: {} (type={})'.format(id, item.image, type(item.image)))
    if not item.image:
        raise Http404
    return HttpResponse(item.image)

'''get_edit_modules: request-> HTTP response: from XML request in well_of_maxwell.js,
recieves all existing non experimental modules and associated content. Displays
using AJAX.'''
def get_edit_modules(request):
    all_modules = Module.objects.all()
    all_content = Content.objects.all()
    all_text = Text.objects.all()
    all_images = Image.objects.all()
    full_dict = dict()
    pre_dumps = []
    for i in range(len(all_modules)):
        item = all_modules[i]
        curr_dict = dict()
        curr_dict['page_title'] = item.page_title
        curr_dict['page_image'] = item.page_image.name
        curr_dict['id'] = item.id
        curr_dict['module_type'] = item.module_type
        curr_dict['number'] = item.number
        pre_dumps.append(curr_dict)
    full_dict['modules'] = pre_dumps
    pre_dumps2 = []
    for i in range(len(all_content)):
        item = all_content[i]
        curr_dict = dict()
        curr_dict['section_title'] = item.section_title
        curr_dict['module_id'] = item.module.id
        curr_dict['id'] = item.id
        pre_dumps2.append(curr_dict)
    full_dict['content']=pre_dumps2
    pre_dumps3 = []
    for i in range(len(all_text)):
        item = all_text[i]
        curr_dict = dict()
        curr_dict['text'] = item.text
        curr_dict['content_id'] = item.content_block.id
        curr_dict['module_id'] = item.content_block.module.id
        curr_dict['id'] = item.id
        pre_dumps3.append(curr_dict)
    full_dict['text'] = pre_dumps3
    pre_dumps4 = []
    for i in range(len(all_images)):
        item = all_images[i]
        curr_dict = dict()
        curr_dict['image'] = item.image.name
        curr_dict['content_id'] = item.content_block.id
        curr_dict['module_id'] = item.content_block.module.id
        curr_dict['id'] = item.id
        pre_dumps4.append(curr_dict)
    full_dict['image'] = pre_dumps4
    json_object = json.dumps(full_dict)
    return HttpResponse(json_object,content_type='application/json')

#delete_module: request -> HTTP response: Deletes the module sent to be deleted, 
#along with ALL content and text associated    
def delete_module(request):
    module = Module.objects.get(id=int(request.POST['module_id']))
    deleted_number = module.number
    deleted_type = module.module_type
    L1 = []
    L2 = []
    for content in Content.objects.all():
        if content.module.id == module.id:
            L1.append(content)
    for text in Text.objects.all():
        for content in L1:
            if text.content_block.id == content.id:
                L2.append(text)
    for curr_content in L1:
        curr_content.delete()
    for curr_text in L2:
        curr_text.delete()
    module.delete()
    for module in Module.objects.all():
        if deleted_type == module.module_type:
            if(deleted_number<module.number):
                module.number = module.number-1
                module.save()
    return HttpResponse(json.dumps(dict()),content_type='application/json')

'''add_content: request -> HTTP response: adds a new content block and routes to XML
redirector function.'''
def add_content(request):
    new_item = Content()
    new_item.section_title = request.POST['section_title']
    related_module = Module.objects.get(id=int(request.POST['module_id']))
    new_item.module= related_module
    new_item.save()
    return grab_content(new_item,related_module)

'''grab_content: (content object, module object) -> HTTP response: similar
as grab module, but returns content instead.'''
def grab_content(content,module):
    new_dict = dict()
    curr_module = dict()
    curr_module['page_title'] = module.page_title
    pre_dumps = [curr_module]
    curr_content = dict()
    curr_content['section_title'] = content.section_title
    curr_content['module_id'] = content.module.id
    pre_dumps2 = [curr_content]
    new_dict['module'] = pre_dumps
    new_dict['content'] = pre_dumps2
    json_object = json.dumps(new_dict)
    return HttpResponse(json_object,content_type='application/json')

'''add_content: request -> HTTP response: adds a new text block and routes to XML
redirector function.'''
def add_text(request):
    new_item = Text()
    new_item.text = request.POST['text']
    related_content = Content.objects.get(id=int(request.POST['content_id']))
    new_item.content_block = related_content
    new_item.save()
    return grab_text(new_item,related_content)

'''grab_content: (content object, module object) -> HTTP response: similar
as grab content, but returns text content instead.'''
def grab_text(text,content):
    new_dict = dict()
    curr_content = dict()
    curr_content['section_title'] = content.section_title
    curr_content['module_id'] = content.module.id
    pre_dumps = [curr_content]
    curr_text = dict()
    curr_text['text'] = text.text
    curr_text['content_id'] = text.content_block.id
    pre_dumps2 = [curr_text]
    new_dict['content'] = pre_dumps
    new_dict['text'] = pre_dumps2
    json_object = json.dumps(new_dict)
    return HttpResponse(json_object,content_type='application/json')

'''grab_image: (content object, module object) -> HTTP response: similar
as grab image, but returns image content instead.'''
def grab_image(image,content):
    new_dict = dict()
    curr_content = dict()
    curr_content['section_title'] = content.section_title
    curr_content['module_id'] = content.module.id
    pre_dumps = [curr_content]
    curr_image = dict()
    curr_image['image'] = image.id
    curr_image['content_id'] = image.content_block.id
    pre_dumps2 = [curr_image]
    new_dict['content'] = pre_dumps
    new_dict['image'] = pre_dumps2
    json_object = json.dumps(new_dict)
    return HttpResponse(json_object,content_type='application/json')

'''add_module_action: request, int -> web page: after submitting to 
Django ModelForm on edit-home.html, redirects here. Creates a new module object.'''
def add_module_action(request,module_type):
    if (request.method == "POST"):
        form = ModuleForm(request.POST,request.FILES)
        if not form.is_valid():
            context = {'form':form}
            return render(request,'well_of_maxwell/edit_home.html',context)
        page_title = form.cleaned_data['page_title']
        page_image = form.cleaned_data['page_image']
        difficulty = form.cleaned_data['difficulty']
        count = 1
        for module in Module.objects.all():
            if module.module_type == module_type and module.difficulty == difficulty:
                count+=1
        new_module = Module()
        new_module.page_title = page_title
        new_module.page_image = page_image
        new_module.module_type = module_type
        new_module.number = count
        new_module.difficulty = difficulty
        new_module.save()
        context = initial_context()
        if(module_type == 0):
            return redirect ('edit-home')
        elif(module_type == 1):
            return redirect ('edit-exp1')
        elif(module_type == 2):
            return redirect ('edit-exp2')
'''edit_exp1_action: request -> web page: renders edit exp1 pages with module 
creation Django form '''
def edit_exp1_action(request):
    if (request.method == "GET"):
        context = {'form':ModuleForm(),
                   }
        return render(request, 'well_of_maxwell/edit_exp1.html',context)

'''edit_exp1_action: request -> web page: renders edit exp2 pages with module 
creation Django form '''
def edit_exp2_action(request):
    if (request.method == "GET"):
        context = {'form':ModuleForm(),
                   }
        return render(request, 'well_of_maxwell/edit_exp2.html',context)

'''add_quiz_action: request, int -> web page: after submitting to 
Django QuizForm on edit-home.html, redirects here. Creates a new quiz object.'''
def add_quiz_action(request):
    if(request.method== "POST"):
        form = QuizForm(request.POST,request.FILES)
        if not form.is_valid():
            context = {'form':form}
            return render(request,'well_of_maxwell/edit_quiz.html',context)
        question = form.cleaned_data['question']
        correct = form.cleaned_data['correct']
        number = form.cleaned_data['number']
        new_quiz = Quiz(question = question)
        new_quiz.number = number
        new_quiz.save()
        #adding the answer objects
        answers = form.cleaned_data.get('answer_choices')
        temp_answer_list = answers.split(',')
        answer_list = []
        for item in temp_answer_list:
            stripped = item.strip()
            answer_list.append(stripped)
        answer_choices = []
        for item in answer_list:
            new_answer = QuizAnswer(text = item)
            new_answer.quiz_block = new_quiz
            new_answer.save()
            answer_choices.append(new_answer)
        check = False
        for answer in answer_choices:
            if (check):
                break
            if answer.text == form.cleaned_data['correct']:
                target = answer
                check = True
        new_quiz.correct = target.text
        new_quiz.save()
        return redirect('edit-quiz')

'''edit_quiz_action: request, int -> web page: adds new question into overall
quiz framework'''
def edit_quiz_action(request):
    if (request.method == "GET"):
        quizzes = []
        answers = set()
        #Invariant: quiz must have problems up to the highest problem number
        largest = 0
        for quiz in Quiz.objects.all():
            curr_number = quiz.number
            if (curr_number>largest):
                largest = curr_number
        for number in range(1,largest+1):
            for quiz in Quiz.objects.all():
                if quiz.number == number:
                    quizzes.append(quiz)
                    curr_number+=1
        for answer in QuizAnswer.objects.all():
            for quiz in quizzes:
                if answer.quiz_block.id == quiz.id:
                    answers.add(answer)
                
        context = {'form':QuizForm(), 'quizzes':quizzes, 'answers':answers}
        return render(request, 'well_of_maxwell/edit_quiz.html',context)

'''
INTEGRATION
##################################################################################################################################

##################################################################################################################################
'''

#read_voltage_exp1: dummy function to return a proper htpp reseponse 
def read_voltage_exp1(request):
    json_object = json.dumps(dict())
    return HttpResponse(json_object,content_type='application/json')

#get_voltage_exp1: request -> htpp response: generates new plot object based on
#current image stored in database, and returns this object to well_of_maxwell.js
def get_voltage_exp1(request):
    curr_voltages = dict()
    voltage = []
    sample = []
    voltage_string = ""
    while (len(Plot.objects.all())>5):
        Plot.objects.all()[0].delete()

    new_plot = Plot()
    new_plot.image.name = "plot1.png"
    new_plot.save()
    curr_voltages['photo_id'] = new_plot.id

    json_object = json.dumps(curr_voltages)
    return HttpResponse(json_object,content_type='application/json')
    
#read_voltage_exp1: dummy function to return a proper htpp reseponse 
def read_voltage_exp2(request):
    json_object = json.dumps(dict())
    return HttpResponse(json_object,content_type='application/json')

#get_voltage_exp2: request -> htpp response: filters the voltage data based on
#data in CSV file, and determines which image to assign to the current outputs. 
def get_voltage_exp2(request):
    curr_voltages = dict()
    voltage = []
    sample = []
    voltage_string = ""
    i = 0
    sample_rate = 40000
    with open('well_of_maxwell/example.csv','r') as csvfile:
        reader = csv.reader(csvfile, delimiter= ' ', quotechar='|')
        for row in reader:
            #print(row)
            if i != 0:
                if(len(row)==1):
                    continue
                else:
                    sample.append(row[0])
                    voltage.append(float(row[1]))
            i+=1
    if(len(voltage)==0):
        curr_voltages['voltage'] = voltage[0:10]
        curr_voltages['highest'] = 0
        curr_voltages['lowest'] = 0
        curr_voltages['pp'] = 0
    else:
        highest = max(voltage)
        lowest = min(voltage)
        pp = highest - lowest
        count = 0
        average_list = []
        while len(voltage)< sample_rate:
            voltage.append(voltage[-1])
        for i in range(10):
            curr = 0
            for j in range(sample_rate//10):
                curr += voltage[count]
                count +=1
            average_list.append(round(curr/(sample_rate//10), 3))
        curr_voltages['voltage'] = average_list
        curr_voltages['highest'] = highest
        curr_voltages['lowest'] = lowest
        curr_voltages['pp'] = pp
    while (len(Plot.objects.all())>5):
        Plot.objects.all()[0].delete()
    total=0
    for value in average_list:
        total+= float(value)
    new_plot = Plot()
    if (round(total/(len(curr_voltages))) < -1):
        new_plot.image.name = "flip2.png"
    elif (round(total/(len(curr_voltages))) > 1):
        new_plot.image.name = "flip1.png"
    else:
        new_plot.image.name ="flip3.png"
    new_plot.save()
    curr_voltages['photo_id'] = new_plot.id

    json_object = json.dumps(curr_voltages)
    return HttpResponse(json_object,content_type='application/json')

#get_plot: request, int -> HTTP repsonse: returns properly formatted image data for
#the two experiment plots.
def get_plot(request,id):
    item = get_object_or_404(Plot,id=id)
    print('Picture #{} fetched from db: {} (type={})'.format(id, item.image, type(item.image)))
    if not item.image:
        raise Http404
    return HttpResponse(item.image)
