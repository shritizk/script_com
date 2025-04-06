from django.contrib import admin
from django.urls import path , include

# views
from .views import *

urlpatterns = [
    path('',home_page)
]
