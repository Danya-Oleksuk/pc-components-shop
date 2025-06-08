from django.test import TestCase
from django.urls import reverse


class InfoViewsTestCase(TestCase):

    def test_about_view(self):
        response = self.client.get(reverse("info:about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "info/about.html")

    def test_contacts_view(self):
        response = self.client.get(reverse("info:contacts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "info/contacts.html")

    def test_terms_view(self):
        response = self.client.get(reverse("info:terms"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "info/terms.html")
