from django.contrib import admin
from django.urls import path , include

# views
from .views import *

urlpatterns = [
    path('',explore_page),
    path('<uuid:id>/', script_explore ),
    path('upvore/<uuid:id>/',upvote)
]
