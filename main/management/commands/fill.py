from django.core.management import BaseCommand

from main.models import Student


class Command(BaseCommand):

    def handle(self, *args, **options):
        students_list = [{'first_name': 'Oleg', 'last_name': 'Maslov'},
                         {'first_name': 'Aleksey', 'last_name': 'Matyuk'},
                         {'first_name': 'Julia', 'last_name': 'Blokhina'}]

        students_objects = []

        for student_item in students_list:
            students_objects.append(Student(**student_item))
            # Student.objects.create(**student_item)

        Student.objects.bulk_create(students_objects)
