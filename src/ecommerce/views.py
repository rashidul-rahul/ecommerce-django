from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ContactForm


def home_page(request):
    context = {
        "brand_name": "Ecommerce"
    }
    return render(request, "home.html", context=context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    return render(request, "contact.html", context=context)


def login_page(request):
    form = LoginForm(request.POST or None)

    context = {
        "form": form
    }
    print(request.user.is_authenticated())
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect("/")
        else:
            print("Error")
    return render(request, "auth/login.html", context=context)


User = get_user_model()


def register_page(request):
    form = RegistrationForm(request.POST or None)

    context = {
        "form": form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create_user(username, email, password)
        print(new_user)
    return render(request, "auth/register.html", context=context)
