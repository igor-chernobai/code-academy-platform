from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('course/<int:course_id>/lesson/<slug:slug>/', views.StudentLessonRetrieveAPIView.as_view()),
    path('course/<int:course_id>/', views.StudentLessonRetrieveAPIView.as_view()),
    # path('lesson/<int:pk>/', views.StudentLessonRetrieveAPIView.as_view())
]
