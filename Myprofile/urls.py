from django.contrib import admin
from django.urls import path , include

# views
from .views import *

urlpatterns = [
    path('',main),
    path('profile',profile), # this page will give user code and render stuff same as it does in the explore one 
    path('sender',prof_email), # this is to send key to the email to access  
    path('delete/<str:id>',delete_script),
]
