from django.db import models

# null=True, blank=True это значит что данное поле может быть пустым, т.е. аватар не обязателен
NULLABLE = {'blank': True, 'null': True}


class Student(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='имя')  # обязательно
    last_name = models.CharField(max_length=150, verbose_name='фамилия')  # обязательно
    avatar = models.ImageField(upload_to='students/', verbose_name='аватар',
                               **NULLABLE)  # не обязательно т.к. есть **NULLABLE
    # для email у моделей есть специяльное поле, здесь такой метод применен для эксперимента
    email = models.CharField(max_length=150, verbose_name='@email', unique=True, **NULLABLE)
    comment = models.TextField(verbose_name='комментарий менеджера', **NULLABLE)

    is_active = models.BooleanField(default=True, verbose_name='активный')

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

    # def delete(self, *args, **kwargs):
    #     """Переопределение метода delete, теперь он деактивирует записи"""
    #     self.is_active = False
    #     self.save()

    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'студенты'
        ordering = ('last_name',)


class Subject(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='студент')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'предметы'
