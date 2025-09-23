from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils.text import slugify
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import User
from cart.models import Cart
from products.models import Product, Category


class CartViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuseremail@gmail.com", password="testpass"
        )

        self.category = Category.objects.create(name="Test Category")

        empty_image = SimpleUploadedFile(
            name="test_image.jpg", content=b"", content_type="image/jpeg"
        )

        self.product = Product.objects.create(
            name="Test Product",
            slug=slugify("Test Product"),
            description="Test description",
            price=Decimal("100.00"),
            image=empty_image,
            available=True,
            category=self.category,
        )
        self.cart = Cart.objects.create(user=self.user, product_id=self.product.id)

    def test_list_carts_unauthorized(self):
        url = reverse("cart-view-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_cart_unauthorized(self):
        url = reverse("cart-view-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_carts_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("cart-view-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_retrieve_cart_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("cart-view-detail", args=[self.cart.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
