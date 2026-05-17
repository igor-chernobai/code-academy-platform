from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField('email', unique=True)
    photo = models.ImageField('зображення', upload_to='users/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class StudentProgress(models.Model):
    student = models.ForeignKey(get_user_model(),
                                on_delete=models.CASCADE,
                                verbose_name='користувач')
    lesson = models.ForeignKey('courses.Lesson',
                               on_delete=models.CASCADE,
                               verbose_name='лекція')
    is_complete = models.BooleanField('завершено?')
    complete_at = models.DateTimeField('дата завершення лекції', auto_now_add=True)

    class Meta:
        db_table = 'lesson_progress'
        verbose_name = 'прогрес лекції'
        verbose_name_plural = 'прогрес лекцій'

        constraints = [
            models.UniqueConstraint(fields=['student', 'lesson'], name='unique_student_progress')
        ]

    def __str__(self):
        status = 'Завершено' if self.is_complete else 'Не завершено'
        return f'{self.student} - {self.lesson} ({status})'
