from django.shortcuts import render, redirect
from .models import Cart
from products.models import Product


def cart_home(request):
    cart, check = Cart.objects.get_or_new(request)
    return render(request, 'cart/view.html', {"cart": cart})


def cart_update(request):
    if request.method == "POST":
        product_id = request.POST["product"]
        if product_id is not None:
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                print("message user that it gone")
                redirect("cart:home")

            cart, is_new = Cart.objects.get_or_new(request)
            if product in cart.products.all():
                cart.products.remove(product)
            else:
                cart.products.add(product)

        request.session["cart_items"] = cart.products.count()
    return redirect("cart:home")
