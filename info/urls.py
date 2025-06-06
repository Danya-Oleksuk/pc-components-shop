from django.urls import path

from .views import AboutView, ContactsView, TermsView

app_name = "info"

urlpatterns = [
    path("about/", AboutView.as_view(), name="about"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("terms/", TermsView.as_view(), name="terms"),
]