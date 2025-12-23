from django.urls import path

from api.v2.users import views


app_name = "users"

urlpatterns = [
    path("", views.UserListApi.as_view(), name="user-list"),
    path(
        "token/obtain/", views.AuthTokenObtainView.as_view(), name="user-token-obtain"
    ),
]
