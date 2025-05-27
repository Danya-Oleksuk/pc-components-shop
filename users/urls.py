from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('test/', views.UserRegisterView.as_view(), name='register'),
    path('profile/', views.UserRegisterView.as_view(), name='profile'),
]