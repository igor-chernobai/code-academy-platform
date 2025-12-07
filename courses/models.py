from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from markdown import markdown
from mdeditor.fields import MDTextField


class Course(models.Model):
    title = models.CharField("назва курса", max_length=155)
    slug = models.SlugField("слаг", max_length=155)
    created = models.DateTimeField("дата створення курсу", auto_now_add=True)
    image = models.ImageField("зображення", upload_to="course_image/", blank=True, null=True)
    short_description = models.TextField("коротко про курс")
    about = models.TextField("про курс")
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name="власник")
    students = models.ManyToManyField(get_user_model(), related_name="courses_joined", blank=True)

    class Meta:
        db_table = "course"
        verbose_name = "курс"
        verbose_name_plural = "курси"

    def get_absolute_url(self):
        return reverse("courses:course_detail", args=[self.slug])

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name="modules",
                               verbose_name="курс")
    title = models.CharField("назва модулю", max_length=155)
    slug = models.SlugField("слаг", max_length=155)
    created = models.DateTimeField("дата створення модулю", auto_now_add=True)
    note = models.TextField("опис модулю")
    order = models.PositiveIntegerField("порядок", null=True)

    class Meta:
        db_table = "module"
        verbose_name = "модуль"
        verbose_name_plural = "модулі"
        ordering = ["order"]

    @property
    def get_next_module(self):
        next_modules = self.course.modules.filter(order__gt=self.order)
        if next_modules.exists():
            return next_modules.first()
        return None

    def __str__(self):
        return self.title


class Lesson(models.Model):
    module = models.ForeignKey(Module,
                               on_delete=models.CASCADE,
                               related_name="lessons",
                               verbose_name="модуль")
    title = models.CharField("назва теми", max_length=155)
    slug = models.SlugField("слаг", max_length=155)
    content = MDTextField()
    created = models.DateTimeField("дата створення теми", auto_now_add=True)
    order = models.PositiveIntegerField("порядок")

    class Meta:
        db_table = "lesson"
        verbose_name = "лекція"
        verbose_name_plural = "лекції"
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(fields=["module", "order"], name="unique_lesson_order")
        ]

    @property
    def get_next(self):
        next_lessons = self.module.lessons.filter(order__gt=self.order)
        if next_lessons.exists():
            return next_lessons.first()
        else:
            next_module = self.module.get_next_module
            if next_module:
                return next_module.lessons.first()

        return None

    def content_formatted(self):
        return mark_safe(
            markdown(self.content,
                     extensions=['extra', 'fenced_code', 'codehilite', 'toc'],
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
