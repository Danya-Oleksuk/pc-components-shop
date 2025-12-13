from django.test import TestCase

from orders.tests import User
from users.forms import UserLoginForm, UserRegisterForm


class UserModelTest(TestCase):
    def test_create_user_with_email(self):
        email = "testuser@example.com"
        password = "password123"

        user = User.objects.create(email=email)
        user.set_password(password)
        user.save()

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.get_username(), email)

    def test_create_user_with_no_email(self):
        with self.assertRaises(ValueError):
            User.objects.create(email="")

        with self.assertRaises(ValueError):
            User.objects.create(email=None)

    def test_create_superuser(self):
        email = "admin@example.com"
        password = "adminpassword123"

        admin_user = User.objects.create(
            email=email, password=password, is_staff=True, is_superuser=True
        )

        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
        self.assertEqual(admin_user.email, email)

    def test_user_email_is_unique(self):
        email = "testuser@example.com"
        password = "password123"

        User.objects.create(
            email=email,
            password=password,
        )

        with self.assertRaises(Exception):
            User.objects.create(
                email=email,
                password="newpassword123",
            )


class UserLoginFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="testuser@example.com",
        )
        self.user.set_password("testpassword")
        self.user.save()

    def test_login_form_valid(self):
        form_data = {"username": "testuser@example.com", "password": "testpassword"}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form_data = {"username": "testuser@example.com", "password": "wrongpassword"}
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_login_user_authenticated(self):
        form_data = {"username": "testuser@example.com", "password": "testpassword"}
        form = UserLoginForm(data=form_data)

        self.assertTrue(form.is_valid())
        user = form.get_user()
        self.assertEqual(user.email, self.user.email)


class UserRegisterFormTest(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

    def test_register_form_valid(self):
        form = UserRegisterForm(data=self.user_data)
        self.assertTrue(form.is_valid())

    def test_register_form_invalid_passwords_not_matching(self):
        form_data = {
            "email": "testuser@example.com",
            "password1": "testpassword",
            "password2": "wrongpassword",
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_register_user_creation(self):
        form = UserRegisterForm(data=self.user_data)
        self.assertTrue(form.is_valid())
        user = form.save()

        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password1"]))

    def test_register_user_email_unique(self):
        form = UserRegisterForm(data=self.user_data)
        form.save()

        form_data = {
            "email": "testuser@example.com",
            "password1": "anotherpassword",
            "password2": "anotherpassword",
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
