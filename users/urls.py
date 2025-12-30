from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("enroll-course/", views.StudentEnrollCourseView.as_view(), name="student_enroll_course"),
    path("courses/", views.StudentCourseListView.as_view(), name="student_course_list"),
    path("course/<int:course_id>/", views.StudentLessonDetailView.as_view(), name="student_course"),
    path("course/<int:course_id>/<slug:lesson_slug>/", views.StudentLessonDetailView.as_view(),
         name="student_course_lesson"),
    path("lesson/complete/", views.LessonCompleteView.as_view(), name="lesson_complete"),
    path('profile/', views.StudentProfileView.as_view(), name='profile')
]
