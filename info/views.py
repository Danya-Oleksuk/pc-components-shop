from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import ContactMessage
from .forms import ContactForm


class AboutView(TemplateView):
    template_name = "info/about.html"


class ContactsView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = 'info/contacts.html'
    success_url = reverse_lazy('info:contacts')


class TermsView(TemplateView):
    template_name = "info/terms.html"
