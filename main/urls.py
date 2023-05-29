from django.urls import path

from main.apps import MainConfig
from main.views import index, contacts, students, student

app_name = MainConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', contacts, name='contacts'),
    path('students/', students, name='students_list'),
    path('student/<int:pk>/', student, name='student_item'),
]
