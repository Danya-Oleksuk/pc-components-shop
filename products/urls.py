from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('', views.MainPageView.as_view(), name='profile'),
    path('', views.MainPageView.as_view(), name='login'),
    path('', views.MainPageView.as_view(), name='register'),
    path('', views.MainPageView.as_view(), name='cart'),
    path('', views.MainPageView.as_view(), name='catalog'),
]