from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path('lesson/<slug:slug>/', views.lesson_detail, name="lesson"),
    path("lesson/<slug:slug>/complete/", views.lesson_complete, name="lesson_complete")
]
