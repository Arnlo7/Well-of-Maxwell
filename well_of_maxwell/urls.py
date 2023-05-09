from django.urls import path, include
from django.contrib.auth import views as auth_views
from well_of_maxwell import views

'''
urls.py: functions as redirector between views and controller; recieves HTTP request
from web pages and directs the HTTP requests to proper handelers in views.py based on
current URL patterns. 
'''

urlpatterns = [
    path('', views.welcome_action, name='welcome'),
    path('login-complete', views.login_complete_action, name='login-complete'),
    path('difficulty', views.difficulty_action, name = 'difficulty'),
    path('hub', views.hub_action, name = "hub"),
    path('home-hub/<int:difficulty>', views.home_hub_action, name = "home-hub"),
    path('home/<int:id>/<int:difficulty>', views.home_action, name = "home"),
    path('exp1/<int:id>/<int:difficulty>', views.exp1_action, name = "exp1"),
    path('exp2/<int:id>/<int:difficulty>', views.exp2_action, name = "exp2"),
    path('exp1-hub', views.exp1_hub_action, name = "exp1-hub"),
    path('exp2-hub', views.exp2_hub_action, name = "exp2-hub"),
    path('quiz-start', views.quiz_start_action, name = "quiz-start"),
    path('quiz/<int:number>', views.quiz_action, name = "quiz"),
    path('reset-quiz', views.reset_quiz_action, name = "reset-quiz"),
    path('parse-quiz/<int:number>/<int:score_id>/<int:correct>', views.parse_quiz, name = "parse-quiz"),
    path('edit-home', views.edit_home_action, name = "edit-home"),
    path('edit-exp1', views.edit_exp1_action, name = "edit-exp1"),
    path('edit-exp2', views.edit_exp2_action, name = "edit-exp2"),
    path('edit-quiz', views.edit_quiz_action, name = "edit-quiz"),
    path('exp1-end', views.exp1_end_action, name="exp1-end"),
    path('exp2-end', views.exp2_end_action, name="exp2-end"),
    path('admin', views.admin_action, name = "admin"),
    path('welcome', views.welcome_action, name='welcome'),
    path('get-edit-modules', views.get_edit_modules,name = 'get-edit-modules'),
    path('add-quiz',views.add_quiz_action,name='add-quiz'),
    path('add-module/<int:module_type>', views.add_module_action,name='add-module'),
    path('delete-module', views.delete_module,name='delete-module'),
    path('add-content', views.add_content,name='add-content'),
    path('add-text',views.add_text,name='add-content'),
    path('add-image/<int:content_id>/<int:home_id>/<int:difficulty>',views.add_image_action,name='add-image'),
    path('add-exercise/<int:content_id>/<int:home_id>/<int:difficulty>',views.add_exercise_action,name='add-exercise'),
    path('get-module-photo/<int:id>',views.get_module_photo,name='get-module-photo'),
    path('get-content-photo/<int:id>',views.get_content_photo,name='get-content-photo'),
    #INTEGRATION URLs
    path('get-voltage-exp1', views.get_voltage_exp1, name='get-voltage-exp1'),
    path('read-voltage-exp1', views.read_voltage_exp1, name='read-voltage-exp1'),
    path('get-voltage-exp2', views.get_voltage_exp2, name='get-voltage-exp2'),
    path('read-voltage-exp2', views.read_voltage_exp2, name='read-voltage-exp2'),
    path('get-plot/<int:id>', views.get_plot, name = 'get-plot')
]