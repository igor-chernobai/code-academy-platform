from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password_change/", views.StudentPasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", views.StudentPasswordChangeDoneView.as_view(), name="password_change_done"),
    path("enroll-course/", views.StudentEnrollCourseView.as_view(), name="student_enroll_course"),
    path("courses/", views.StudentCourseListView.as_view(), name="student_course_list"),
    path("course/<int:course_id>/", views.StudentLessonDetailView.as_view(), name="student_course"),
    path("course/<int:course_id>/<slug:lesson_slug>/", views.StudentLessonDetailView.as_view(),
         name="student_course_lesson"),
    path("lesson/complete/", views.LessonCompleteView.as_view(), name="lesson_complete")
]
