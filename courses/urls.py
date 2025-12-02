from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("<slug:slug>/", views.CourseDetailView.as_view(), name="course_detail"),
]
