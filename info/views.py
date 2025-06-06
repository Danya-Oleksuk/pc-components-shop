from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "info/about.html"

class ContactsView(TemplateView):
    template_name = "info/contacts.html"

class TermsView(TemplateView):
    template_name = "info/terms.html"