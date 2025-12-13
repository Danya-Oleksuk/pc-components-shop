from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)
from django.utils.translation import gettext_lazy as _

from users.models.users import User


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Емаїл"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Введіть свою електронну адресу"),
            }
        ),
    )
    password = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Введіть свій пароль")}
        ),
    )


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Емаїл"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Введіть свою електронну адресу"),
            }
        ),
    )
    password1 = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Введіть свій пароль")}
        ),
    )
    password2 = forms.CharField(
        label=_("Підтвердьте пароль"),
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Підтвердьте свій пароль")}
        ),
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")
