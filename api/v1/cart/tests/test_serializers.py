from decimal import Decimal
from rest_framework.test import APITestCase
from django.utils.text import slugify
from django.core.files.uploadedfile import SimpleUploadedFile

from ..serializers import CartSerializer
from users.models import User
from products.models import Category, Product


class CartSerializerTestCase(APITestCase):

    def setUp(self):
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

    def test_valid_serializer(self):
        test_data = {"product": self.product.id, "quantity": 3}

        serializer = CartSerializer(data=test_data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["product"].id, self.product.id)
        self.assertEqual(serializer.validated_data["quantity"], 3)

    def test_invalid_serializer(self):
        test_data = {"product": "<self.product.id>", "quantity": 3}

        serializer = CartSerializer(data=test_data)

        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn("product", serializer.errors)
        self.assertNotIn("quantity", serializer.errors)

    def test_invalid_quantity(self):
        test_data = {"product": self.product.id, "quantity": -1}

        serializer = CartSerializer(data=test_data)

        self.assertFalse(serializer.is_valid(), serializer.errors)
        self.assertIn("quantity", serializer.errors)
