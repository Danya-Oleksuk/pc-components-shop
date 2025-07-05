from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register('products', ProductViewSet)

app_name = 'api'
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', obtain_auth_token),
]