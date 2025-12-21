from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from products.models.category import Category
from products.models.product import Product
from users.models.users import User

from .urls import (
    get_product_create_url,
    get_product_update_url,
    get_product_delete_url,
)


class ProductApiUnathorizedTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        category_data = {
            "name": "Smartphones",
            "description": "test",
        }
        self.category = Category.objects.create(**category_data)

        product_data = {
            "name": "Iphone 12",
            "price": 1000,
            "description": "test",
            "category": self.category,
        }
        self.product = Product.objects.create(**product_data)

    def test_product_create_unathorized(self):
        response = self.client.post(get_product_create_url())

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_update_unathorized(self):
        response = self.client.patch(get_product_update_url(self.product.id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_delete_unathorized(self):
        response = self.client.delete(get_product_delete_url(self.product.id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductApiAuthorizedTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(
            email="test@gmail.com",
            password="testPassword",
        )
        self.user.is_staff = True
        self.user.save()

        category_data = {
            "name": "Smartphones",
            "description": "test",
        }
        self.category = Category.objects.create(**category_data)

        product_data = {
            "name": "Iphone 12",
            "price": 1000,
            "description": "test",
            "category": self.category,
        }
        self.product = Product.objects.create(**product_data)

    def test_product_create_authorized(self):
        payload = {
            "name": "Iphone 16",
            "price": 1000,
            "description": "test",
            "available": True,
            "category": self.category.id,
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(get_product_create_url(), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Iphone 16")
        self.assertEqual(response.data["price"], "1000.00")

    def test_product_update_authorized(self):
        payload = {
            "name": "Iphone 18",
            "price": 1200,
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            get_product_update_url(self.product.id), payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Iphone 18")
        self.assertEqual(response.data["price"], "1200.00")

    def test_product_delete_authorized(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(get_product_delete_url(self.product.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
