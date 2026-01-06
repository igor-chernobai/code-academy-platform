from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('course/<int:course_id>/lesson/<slug:slug>/', views.StudentLessonRetrieveAPIView.as_view()),
    path('course/<int:course_id>/', views.StudentLessonRetrieveAPIView.as_view()),
    path('auth-token/', obtain_auth_token),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', jwt_views.TokenBlacklistView.as_view()),
    path('subscription/', views.SubscriptionDetail.as_view()),
]
