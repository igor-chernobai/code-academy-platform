from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from courses.models import Course, Lesson


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Ім'я студента",
                               widget=forms.TextInput(attrs={
                                   "class": "w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={
                                   "class": "w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Ім'я студента",
                               widget=forms.TextInput(attrs={
                                   "class": "w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"}))
    first_name = forms.CharField(label="Ім'я",
                                 widget=forms.TextInput(attrs={
                                     "class": "w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"}))
    password1 = forms.CharField(label="Пароль",
                                widget=forms.PasswordInput(attrs={
                                    "class": "w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"}))
    password2 = forms.CharField(label="Повторіть пароль",
                                widget=forms.PasswordInput(attrs={
                                    "class": "w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"}))

    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "password1", "password2"]


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

    #
    # def save(self):
    #     lesson = self.cleaned_data["lesson"]
    #     LessonProgress.objects.get_or_create(student=self.student,
    #                                          lesson=lesson,
    #                                          defaults={"is_complete": True})
    #     return lesson
