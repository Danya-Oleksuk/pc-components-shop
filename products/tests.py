from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Product, Category


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

    def test_filter_by_category(self):
        category_gpu = Category.objects.create(name="Видеокарты")
        category_cpu = Category.objects.create(name="Процессоры")

        Product.objects.create(name="RTX 3080", price=70000, category=category_gpu)
        Product.objects.create(name="Ryzen 5", price=15000, category=category_cpu)

        response = self.client.get('/products/?category=Видеокарты')
        self.assertContains(response, "RTX 3080")
        self.assertNotContains(response, "Ryzen 5")

    def test_search_products(self):
        Product.objects.create(name="SSD 1TB", price=3000)
        response = self.client.get('/products/?q=SSD')
        self.assertContains(response, "SSD 1TB")

class CategoryModelTest(TestCase):

    def test_category_str(self):
        category = Category.objects.create(name="Відеокарти")
        self.assertEqual(str(category), "Відеокарти")


class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Процесори")

    def test_product_creation_and_slug_generation(self):
        image = SimpleUploadedFile(name='test.jpg', content=b'', content_type='image/jpeg')
        product = Product.objects.create(
            name="Ryzen 5 5600",
            price=5999.99,
            image=image,
            category=self.category
        )
        self.assertEqual(str(product), "Ryzen 5 5600")
        self.assertEqual(product.slug, "ryzen-5-5600")
        self.assertEqual(product.available, True)
        self.assertIsNotNone(product.created_at)

    def test_product_has_category(self):
        image = SimpleUploadedFile(name='test.jpg', content=b'', content_type='image/jpeg')
        product = Product.objects.create(
            name="Intel i5",
            price=6999.99,
            image=image,
            category=self.category
        )
        self.assertEqual(product.category.name, "Процесори")