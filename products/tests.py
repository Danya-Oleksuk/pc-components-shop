from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from products.models.product import Product
from products.models.category import Category


class HomePageTest(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(reverse("products:main_page"))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template_name(self):
        response = self.client.get(reverse("products:main_page"))
        self.assertTemplateUsed(response, "products/main_page.html")


class CatalogTest(TestCase):
    def test_catalog_page_status_code(self):
        response = self.client.get(reverse("products:catalog"))
        self.assertEqual(response.status_code, 200)

    def test_catalog_page_template_name(self):
        response = self.client.get(reverse("products:catalog"))
        self.assertTemplateUsed(response, "products/products_list.html")

    def test_products_are_listed(self):
        response = self.client.get(reverse("products:catalog"))
        self.assertContains(response, "Каталог товарів")
        self.assertContains(response, "Категорії")
        self.assertContains(response, "Фільтр за ціною")


class CategoryModelTest(TestCase):
    def test_category_str(self):
        category = Category.objects.create(name="Відеокарти")
        self.assertEqual(str(category), "Відеокарти")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Процесори")

    def test_product_creation_and_slug_generation(self):
        image = SimpleUploadedFile(
            name="test.jpg", content=b"", content_type="image/jpeg"
        )
        product = Product.objects.create(
            name="Ryzen 5 5600", price=5999.99, image=image, category=self.category
        )
        self.assertEqual(str(product), "Ryzen 5 5600")
        self.assertEqual(product.slug, "ryzen-5-5600")
        self.assertEqual(product.available, True)
        self.assertIsNotNone(product.created_at)

    def test_product_has_category(self):
        image = SimpleUploadedFile(
            name="test.jpg", content=b"", content_type="image/jpeg"
        )
        product = Product.objects.create(
            name="Intel i5", price=6999.99, image=image, category=self.category
        )
        self.assertEqual(product.category.name, "Процесори")
