from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("enroll-course/", views.StudentEnrollCourseView.as_view(), name="student_enroll_course"),
    path("courses/", views.student_course_list, name="student_course_list"),
    path("course/<int:course_id>/", views.student_course_lesson, name="student_course"),
    path("course/<int:course_id>/<slug:lesson_slug>/", views.student_course_lesson, name="student_course_lesson"),
    path("lesson/<slug:slug>/complete/", views.lesson_complete, name="lesson_complete")
]
