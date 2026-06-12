from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from . import views

app_name = "api"

router = DefaultRouter()
router.register(r"courses", views.CourseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("course/<int:course_id>/lesson/<slug:slug>/", views.StudentLessonRetrieveAPIView.as_view()),
    path("course/<int:course_id>/", views.StudentLessonRetrieveAPIView.as_view()),
    # Auth
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", jwt_views.TokenVerifyView.as_view(), name="token_verify"),
    path("token/blacklist/", jwt_views.TokenBlacklistView.as_view()),
    # Users
    path("auth/register/", views.UserCreate.as_view(), name="register"),
    path("users/me/", views.UserMeAPIView.as_view(), name="user-me"),
    path("subscriptions/", views.SubscriptionCreateAPIView.as_view(), name="subscription_create"),
    path("subscriptions/me/", views.SubscriptionRetrieveAPIVIew.as_view(), name="my-subscription"),
    path("subscriptions/update/", views.SubscriptionUpdateAPIView.as_view(), name="subscription_update"),
    path("plans/", views.PlanListAPIView.as_view(), name="plan_list"),
    path("lesson/<int:lesson_id>/complete/", views.LessonCompleteAPIView.as_view(), name="lesson_complete"),
    # Swagger
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="api:schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="api:schema"), name="redoc"),
]
