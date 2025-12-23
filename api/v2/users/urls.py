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
]
