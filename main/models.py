from django.db import models

# null=True, blank=True это значит что данное поле может быть пустым, т.е. аватар не обязателен
NULLABLE = {'blank': True, 'null': True}


class Student(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='имя')  # обязательно
    last_name = models.CharField(max_length=150, verbose_name='фамилия')  # обязательно
    avatar = models.ImageField(upload_to='students/', verbose_name='аватар', **NULLABLE)  # не обязательно т.к. есть **NULLABLE

    comment = models.TextField(verbose_name='комментарий менеджера', **NULLABLE)

    is_active = models.BooleanField(default=True, verbose_name='активный')

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'студенты'
        ordering = ('last_name',)
