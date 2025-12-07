from django import forms
from django.utils.translation import gettext_lazy as _

from orders.models.order import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_("Ім’я"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Ім’я")}
        ),
        required=True,
        error_messages={"required": _("Будь ласка, введіть ваше ім’я.")},
    )
    last_name = forms.CharField(
        label=_("Прізвище"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Прізвище")}
        ),
        required=True,
        error_messages={"required": _("Будь ласка, введіть ваше прізвище.")},
    )
    phone = forms.CharField(
        label=_("Телефон"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Телефон")}
        ),
        required=True,
        error_messages={"required": _("Будь ласка, введіть номер телефону.")},
    )

    city = forms.CharField(
        label=_("Місто"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "city-input",
                "placeholder": _("Місто"),
            }
        ),
        required=True,
        error_messages={"required": _("Будь ласка, введіть назву міста.")},
    )

    warehouse = forms.CharField(
        label=_("Відділення / Поштомат"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "warehouse-input",
                "placeholder": _("Відділення/Поштомат"),
            }
        ),
        required=True,
        error_messages={"required": _("Будь ласка, вкажіть відділення або поштомат.")},
    )

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone.isdigit():
            raise forms.ValidationError(_("Номер телефону повинен містити лише цифри."))
        elif len(phone) < 10:
            raise forms.ValidationError(
                _("Введіть дійсний номер телефону, який містить щонайменше 10 цифр.")
            )
        return phone

    class Meta:
        model = Order
        fields = ("first_name", "last_name", "phone", "city", "warehouse")
