from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

handler404 = "errors.views.custom_404"
handler500 = "errors.views.custom_500"
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("products.urls")),
    path("", include("users.urls")),
    path("", include("cart.urls")),
    path("", include("orders.urls")),
    path("", include("info.urls")),

    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path("", include("products.urls")),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
