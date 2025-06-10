from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "Ваше ім'я", 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': "Ваш Email", 'required': True}),
            'message': forms.Textarea(attrs={'placeholder': "Ваше повідомлення", 'rows': 4, 'required': True}),
        }
