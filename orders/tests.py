from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import resolve, reverse

from orders.forms import OrderForm
from users.models.users import User

from . import views


class OrderFormTests(TestCase):
    def test_valid_form(self):
        data = {
            "first_name": "Іван",
            "last_name": "Петренко",
            "phone": "0981234567",
            "city": "Київ",
            "warehouse": "Відділення 1",
        }
        form = OrderForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_phone_non_digit(self):
        data = {
            "first_name": "Іван",
            "last_name": "Петренко",
            "phone": "09812abc67",
            "city": "Київ",
            "warehouse": "Відділення 1",
        }
        form = OrderForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)
        self.assertEqual(
            form.errors["phone"][0], "Номер телефону повинен містити лише цифри."
        )

    def test_invalid_phone_too_short(self):
        data = {
            "first_name": "Іван",
            "last_name": "Петренко",
            "phone": "12345",
            "city": "Київ",
            "warehouse": "Відділення 1",
        }
        form = OrderForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)
        self.assertEqual(
            form.errors["phone"][0],
            "Введіть дійсний номер телефону, який містить щонайменше 10 цифр.",
        )


class OrdersURLTests(TestCase):
    def test_checkout_url_resolves(self):
        url = reverse("orders:checkout")
        self.assertEqual(resolve(url).func.view_class, views.CheckoutView)

    def test_success_url_resolves(self):
        url = reverse("orders:order_success")
        self.assertEqual(resolve(url).func.view_class, views.SuccessTemplateView)

    def test_cancel_url_resolves(self):
        url = reverse("orders:order_cancel")
        self.assertEqual(resolve(url).func.view_class, views.CancelTemplateView)

    def test_my_orders_url_resolves(self):
        url = reverse("orders:my_orders")
        self.assertEqual(resolve(url).func.view_class, views.MyOrdesView)

    def test_stripe_webhook_url_resolves(self):
        url = reverse("orders:stripe_webhook")
        self.assertEqual(resolve(url).func, views.stripe_webhook)

    def test_autocomplete_city_url_resolves(self):
        url = reverse("orders:autocomplete_city")
        self.assertEqual(resolve(url).func, views.autocomplete_city)

    def test_autocomplete_warehouses_url_resolves(self):
        url = reverse("orders:autocomplete_warehouse")
        self.assertEqual(resolve(url).func, views.autocomplete_warehouses)


class OrdersViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@gmail.com", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")

    def test_checkout_view_get(self):
        response = self.client.get(reverse("orders:checkout"))
        self.assertEqual(response.status_code, 302)

    def test_my_orders_view_get(self):
        response = self.client.get(reverse("orders:my_orders"))
        self.assertEqual(response.status_code, 302)

    def test_cancel_template_view(self):
        response = self.client.get(reverse("orders:order_cancel"))
        self.assertEqual(response.status_code, 302)

    def test_autocomplete_city_view(self):
        response = self.client.get(reverse("orders:autocomplete_city"), {"q": "Київ"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_autocomplete_warehouses_view_without_city_ref(self):
        response = self.client.get(reverse("orders:autocomplete_warehouse"), {"q": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [])

    def test_stripe_webhook_missing_signature(self):
        response = self.client.post(reverse("orders:stripe_webhook"), data={})
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        cache.clear()
