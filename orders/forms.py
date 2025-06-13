from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ім’я"}),
        required=True,
        error_messages={
            'required': 'Будь ласка, введіть ваше ім’я.'
        }
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Прізвище"}),
        required=True,
        error_messages={
            'required': 'Будь ласка, введіть ваше прізвище.'
        }
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Телефон"}),
        required=True,
        error_messages={
            'required': 'Будь ласка, введіть номер телефону.'
        }
    )

    city = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "id": "city-input", "placeholder": "Місто"}),
        required=True,
        error_messages={
            'required': 'Будь ласка, введіть назву міста.'
        }
    )

    warehouse = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "warehouse-input", "placeholder": "Відділення/Поштомат"}),
        required=True,
        error_messages={
            'required': 'Будь ласка, вкажіть відділення або поштомат.'
        }
    )

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if not phone.isdigit():
            raise forms.ValidationError("Номер телефону повинен містити лише цифри.")
        elif len(phone) < 10:
            raise forms.ValidationError(
                "Введіть дійсний номер телефону, який містить щонайменше 10 цифр."
            )
        return phone

    class Meta:
        model = Order
        fields = ("first_name", "last_name", "phone", "city", "warehouse")
