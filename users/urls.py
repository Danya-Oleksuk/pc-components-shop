from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("user/login/", views.UserLoginView.as_view(), name="login"),
    path("user/logout/", views.UserLogoutView.as_view(), name="logout"),
    path("user/register/", views.UserRegisterView.as_view(), name="register"),
    path("user/profile/", views.UserProfileView.as_view(), name="profile"),
    path("user/wishlist/", views.UserWishlist.as_view(), name="wishlist"),
]
