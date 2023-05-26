from django.shortcuts import render

from main.models import Student


def index(request):
    context = {
        'object_list': Student.objects.all()[:3],
        'title': 'Список студентов'
    }
    return render(request, 'main/index.html', context)


def students(request):
    context = {
        'object_list': Student.objects.all(),
        'title': 'Список студентов'
    }
    return render(request, 'main/students.html', context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'User {name}, with email {email}, send message: {message}')
    return render(request, 'main/contact.html')
