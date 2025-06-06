from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ім’я"}),
        required=True,
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Прізвище"}
        ),
        required=True,
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Телефон"}
        ),
        required=True,
    )
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "city-input", "placeholder": "Місто"}
        ),
        required=True,
    )
    warehouse = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "warehouse-input",
                "placeholder": "Відділення/Поштомат",
            }
        ),
        required=True,
    )

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if not phone.isdigit():
            raise forms.ValidationError("Номер телефону повинен містити лише цифри.")
        elif len(phone) < 10:
            raise forms.ValidationError("Введіть дійсний номер телефону, який містить щонайменше 10 цифр.")
        return phone

    class Meta:
        model = Order
        fields = ("first_name", "last_name", "phone", "city", "warehouse")
