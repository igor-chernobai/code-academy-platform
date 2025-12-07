from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from courses.models import Course, Lesson


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Ім'я студента",
                               widget=forms.TextInput(attrs={
                                   "class": "input"}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={
                                   "class": "input"}))


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.HiddenInput
    )


class LessonCompleteForm(forms.Form):
    lesson = forms.ModelChoiceField(
        queryset=Lesson.objects.select_related("module__course").all(),
        widget=forms.HiddenInput
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.HiddenInput
    )

    def clean(self):
        cd = super().clean()
        lesson = cd.get("lesson")
        course = cd.get("course")

        if lesson.module.course != course:
            raise ValidationError("Лекція не відноситься до курсу")
