from django.urls import path

from django_rest_passwordreset.views import (
    reset_password_confirm,
    reset_password_request_token,
    reset_password_validate_token,
)

from api.v2.users import views


app_name = "users"

urlpatterns = [
    path("", views.UserListApi.as_view(), name="user-list"),
    path("me/", views.UserApiView.as_view(), name="user-me"),
    path("create/", views.UserCreateView.as_view(), name="user-create"),
    path("me/update/", views.UserUpdateView.as_view(), name="user-update"),
    path(
        "token/obtain/", views.AuthTokenObtainView.as_view(), name="user-token-obtain"
    ),
    path(
        "password/reset/",
        reset_password_request_token,
        name="user-password-reset",
    ),
    path(
        "password/reset/confirm/",
        reset_password_confirm,
        name="user-password-reset-confirm",
    ),
    path(
        "password/reset/validate/",
        reset_password_validate_token,
        name="user-password-reset-validate",
    ),
    path("<int:pk>/delete/", views.UserDeleteView.as_view(), name="user-delete"),
]
