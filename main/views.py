from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from main.forms import StudentForm, SubjectForm
from main.models import Student, Subject
from main.services import send_deactivate_email


@login_required
def index(request):
    context = {
        'object_list': Student.objects.all()[:3],
        'title': 'Список студентов'
    }
    return render(request, 'main/index.html', context)


class StudentListView(LoginRequiredMixin, generic.ListView):
    model = Student
    extra_context = {
        'title': 'Список студентов'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


# @login_required
# def students(request):
#     context = {
#         'object_list': Student.objects.all(),
#         'title': 'Список студентов'
#     }
#     return render(request, 'main/students.html', context)


class StudentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Student

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # context_data['title'] = context_data['object']
        context_data['title'] = self.get_object()
        return context_data


@login_required
def student(request, pk):
    student_item = Student.objects.get(pk=pk)
    context = {
        'object': student_item,
        'title': student_item.first_name + ' ' + student_item.last_name  # или так 'title': student_item
    }
    return render(request, 'main/student.html', context)


class StudentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Student
    # fields = ('first_name', 'last_name',)
    form_class = StudentForm
    success_url = reverse_lazy('main:students_list')


class StudentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Student
    # fields = ('first_name', 'last_name',)
    form_class = StudentForm
    success_url = reverse_lazy('main:students_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Student, Subject, form=SubjectForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = SubjectFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class StudentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Student
    success_url = reverse_lazy('main:students_list')


@login_required
def toggle_activity(request, pk):
    student_item = get_object_or_404(Student, pk=pk)
    if student_item.is_active:
        student_item.is_active = False
        send_deactivate_email(student_item)
    else:
        student_item.is_active = True

    student_item.save()
    return redirect(reverse('main:student_item', args=[student_item.pk]))


@login_required
def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'User {name}, with email {email}, send message: {message}')
    return render(request, 'main/contact.html')
