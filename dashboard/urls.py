from django.contrib import admin
from django.urls import path , include

# views
from .views import *

urlpatterns = [
    path('',dashboard_page),
    path('myscript/',myscript_page),
    path('newscript',new_script),
    path('edit',edit_req)
]
