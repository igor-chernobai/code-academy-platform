from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
from markdown import markdown
from mdeditor.fields import MDTextField


class Course(models.Model):
    title = models.CharField("Назва курса", max_length=155)
    slug = models.SlugField("Слаг", max_length=155)
    created = models.DateTimeField("Дата створення курсу", auto_now_add=True)
    content = models.TextField("Контент сторінки")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Власник")

    class Meta:
        db_table = "course"
        verbose_name = "Курс"
        verbose_name_plural = "Курси"

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name="modules")
    title = models.CharField("Назва модулю", max_length=155)
    slug = models.SlugField("Слаг", max_length=155)
    created = models.DateTimeField("Дата створення модулю", auto_now_add=True)
    note = models.TextField("Опис модулю")
    order = models.PositiveIntegerField("Порядок", null=True)

    class Meta:
        db_table = "module"
        verbose_name = "Модуль"
        verbose_name_plural = "Модулі"
        ordering = ["order"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, related_name="lessons")
    title = models.CharField("Назва теми", max_length=155)
    slug = models.SlugField("Слаг", max_length=155)
    content = MDTextField()
    created = models.DateTimeField("Дата створення теми", auto_now_add=True)
    order = models.PositiveIntegerField("Порядок", null=True)

    class Meta:
        db_table = "lesson"
        verbose_name = "Лекція"
        verbose_name_plural = "Лекції"
        ordering = ["order"]

    @property
    def get_next(self):
        return Lesson.objects.filter(order__gt=self.order).first()

    def content_formatted(self):
        return mark_safe(
            markdown(self.content,
                     extensions=['extra', 'sane_lists', 'fenced_code', 'nl2br', 'codehilite', 'toc', 'legacy_attrs'],
                     extension_configs={
                         'codehilite': {
                             'linenums': False,
                             'guess_lang': True,
                             'css_class': 'codehilite',
                         }
                     })
        )

    def __str__(self):
        return self.title


class LessonProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Лекція")
    is_complete = models.BooleanField("Завершено?")
    complete_at = models.DateTimeField("Дата завершення лекції", auto_now_add=True)

    class Meta:
        db_table = "lesson_progress"
        verbose_name = "Прогрес лекції"
        verbose_name_plural = "Прогрес лекцій"

    def __str__(self):
        status = "Завершено" if self.is_complete else "Не завершено"
        return f"{self.student} - {self.lesson} ({status})"
