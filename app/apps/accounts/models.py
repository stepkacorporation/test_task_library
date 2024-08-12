from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class RoleChoices(models.TextChoices):
        LIBRARIAN = 'L', 'Библиотекарь'
        READER = 'R', 'Читатель'

    role = models.CharField(max_length=10, choices=RoleChoices, default=RoleChoices.READER, verbose_name='Роль')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Librarian(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE,
        verbose_name='Пользователь', 
        related_name='librarian'
    )
    employee_id = models.CharField(max_length=20, verbose_name='Табельный номер')

    def is_profile_complete(self) -> bool:
        return bool(self.employee_id)

    def __str__(self) -> str:
        return self.user.__str__()

    class Meta:
        verbose_name = 'Библиотекарь'
        verbose_name_plural = 'Библиотекари'


class Reader(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        verbose_name='Пользователь', 
        related_name='reader'
    )
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def is_profile_complete(self) -> bool:
        return bool(self.first_name) and bool(self.last_name) and bool(self.address) 

    def __str__(self) -> str:
        return self.user.__str__()
    
    class Meta:
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'