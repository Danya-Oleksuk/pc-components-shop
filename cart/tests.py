from django.test import TestCase
from django.urls import reverse


class CartURLsTests(TestCase):

    def test_cart_list_url(self):
        url = reverse("cart:cart_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_cart_add_url(self):
        url = reverse("cart:cart_add", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_cart_remove_url(self):
        url = reverse("cart:cart_remove", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

