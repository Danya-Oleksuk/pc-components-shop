from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from orders.models.order import Order
from users.models.users import User

from .urls import (
    get_order_create_url,
    get_order_update_url,
    get_order_delete_url,
)


class OrderApiUnathorizedTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        user_data = {"email": "test@gmail.com", "password": "testPassword"}
        self.user = User.objects.create(**user_data)

        order_data = {
            "user": self.user,
            "total_price": 0,
            "first_name": "test",
            "last_name": "test",
            "city": "test",
            "warehouse": "test",
            "phone": "test",
            "notes": "test",
        }
        self.order = Order.objects.create(**order_data)

    def test_order_create_unathorized(self):
        response = self.client.post(get_order_create_url())

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_update_unathorized(self):
        response = self.client.patch(get_order_update_url(self.order.id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_delete_unathorized(self):
        response = self.client.delete(get_order_delete_url(self.order.id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderApiAuthorizedTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(
            email="test@gmail.com",
            password="testPassword",
        )

        order_data = {
            "user": self.user,
            "total_price": 0,
            "first_name": "test",
            "last_name": "test",
            "city": "test",
            "warehouse": "test",
            "phone": "test",
            "notes": "test",
        }
        self.order = Order.objects.create(**order_data)

    def test_order_create_authorized(self):
        payload = {
            "first_name": "test",
            "last_name": "test",
            "city": "New York",
            "warehouse": "test",
            "phone": 1234567890,
            "notes": "Test notes",
            "total_price": 500,
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(get_order_create_url(), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"], self.user.id)
        self.assertEqual(response.data["city"], "New York")
        self.assertEqual(response.data["total_price"], "500.00")

    def test_order_update_authorized(self):
        payload = {
            "city": "Boston",
            "total_price": 1000,
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            get_order_update_url(self.order.id), payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], self.user.id)
        self.assertEqual(response.data["city"], "Boston")
        self.assertEqual(response.data["total_price"], "1000.00")

    def test_order_delete_authorized(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(get_order_delete_url(self.order.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
