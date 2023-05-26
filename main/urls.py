from django.urls import path

from main.apps import MainConfig
from main.views import index, contacts, students

app_name = MainConfig.name

urlpatterns = [
    path('', index),
    path('contacts/', contacts),
    path('students/', students),
]
