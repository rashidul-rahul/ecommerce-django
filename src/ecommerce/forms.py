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


class RegistrationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control"
    }))

    password2 = forms.CharField(label="Confirm Password",
                                widget=forms.PasswordInput(attrs={
                                    "class": "form-control",
                                }))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        query_set = User.objects.filter(username=username)
        if query_set.exists():
            raise forms.ValidationError("Username already taken")

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        query_set = User.objects.filter(email=email)
        if query_set.exists():
            raise forms.ValidationError("Email already taken")
        return email

    def clean(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Password don't match")

        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Username"
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
    }))

    def clean(self):
        username = self.cleaned_data.get("username")
        if username is None:
            raise forms.ValidationError("Username can't be empty")
        password = self.cleaned_data.get("password")
        if password is None:
            raise forms.ValidationError("Password can't be empty")

        return self.cleaned_data
