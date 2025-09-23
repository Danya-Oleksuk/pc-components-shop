from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsersViewSet, UserRegisterView, UserLoginView, UserLogoutView

router = DefaultRouter()
router.register(r"users", UsersViewSet, basename="users-view")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/user/register/", UserRegisterView.as_view()),
    path("api/user/login/", UserLoginView.as_view()),
    path("api/user/logout/", UserLogoutView.as_view()),
]
