from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Enter Your name"
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Enter your mail"
    }))
    about = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "About"
    }))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if "mail.com" not in email:
            raise forms.ValidationError("Error in mail input")
        return email
