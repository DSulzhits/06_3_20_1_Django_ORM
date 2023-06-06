from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from main.models import Student
from main.services import send_deactivate_email


def index(request):
    context = {
        'object_list': Student.objects.all()[:3],
        'title': 'Список студентов'
    }
    return render(request, 'main/index.html', context)


class StudentListView(generic.ListView):
    model = Student
    extra_context = {
        'title': 'Список студентов'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


# def students(request):
#     context = {
#         'object_list': Student.objects.all(),
#         'title': 'Список студентов'
#     }
#     return render(request, 'main/students.html', context)


class StudentDetailView(generic.DetailView):
    model = Student

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # context_data['title'] = context_data['object']
        context_data['title'] = self.get_object()
        return context_data


# def student(request, pk):
#     student_item = Student.objects.get(pk=pk)
#     context = {
#         'object': student_item,
#         'title': student_item.first_name + ' ' + student_item.last_name  # или так 'title': student_item
#     }
#     return render(request, 'main/student.html', context)


class StudentCreateView(generic.CreateView):
    model = Student
    fields = ('first_name', 'last_name',)
    success_url = reverse_lazy('main:students_list')


class StudentUpdateView(generic.UpdateView):
    model = Student
    fields = ('first_name', 'last_name',)
    success_url = reverse_lazy('main:students_list')


class StudentDeleteView(generic.DeleteView):
    model = Student
    success_url = reverse_lazy('main:students_list')


def toggle_activity(request, pk):
    student_item = get_object_or_404(Student, pk=pk)
    if student_item.is_active:
        student_item.is_active = False
        send_deactivate_email(student_item)
    else:
        student_item.is_active = True

    student_item.save()
    return redirect(reverse('main:student_item', args=[student_item.pk]))


def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'User {name}, with email {email}, send message: {message}')
    return render(request, 'main/contact.html')
