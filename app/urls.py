from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('tracks', tracks, name='tracks'),
    path('apply', apply, name='apply'),
    path('apply-edu', apply_edu, name='apply_edu'),
    path('apply-others', apply_others, name='apply_others'),
    path('continue-login', continue_login, name='continue_login'),
    path('process', process, name='process'),
    path('faq', faq, name='faq'),
    path('application-closed', application_closed, name='application_closed'),
    path('dashboard', dashboard, name='dashbaord'),
    path('referred-landing', referred_landing, name='referred_landing'),
    path('take-test', take_test, name='take_test'),
    path('contact', contact, name='contact'),
]