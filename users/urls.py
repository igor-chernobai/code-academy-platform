from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("password_change/", views.StudentPasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", views.StudentPasswordChangeDoneView.as_view(), name="password_change_done"),

    path("password-reset/",
         auth_views.PasswordResetView.as_view(template_name="users/password_reset_form.html",
                                              email_template_name="users/password_reset_email.html",
                                              success_url=reverse_lazy("users:password_reset_done")),
         name="password_reset"),
    path("password-reset/done/",
         auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name="password_reset_done"),

    path("password-reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html",
                                                     success_url=reverse_lazy("users:password_reset_complete")),
         name="password_reset_confirm"),
    path("password-reset/complete/",
         auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name="password_reset_complete"),

    path("enroll-course/", views.StudentEnrollCourseView.as_view(), name="student_enroll_course"),
    path("courses/", views.StudentCourseListView.as_view(), name="student_course_list"),
    path("course/<int:course_id>/", views.StudentLessonDetailView.as_view(), name="student_course"),
    path("course/<int:course_id>/<slug:lesson_slug>/", views.StudentLessonDetailView.as_view(),
         name="student_course_lesson"),
    path("lesson/complete/", views.LessonCompleteView.as_view(), name="lesson_complete")
]
