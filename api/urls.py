from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'api'

router = SimpleRouter()
router.register(r'courses', views.CourseViewSet)

urlpatterns = [
    path('', include(router.urls))
]
