from decimal import Decimal
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.conf import settings
from products.models import Product


User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def get_or_new(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)

        if qs.count() == 1:
            cart = qs.first()
            new_obj = False
            if cart.user is None and request.user.is_authenticated():
                cart.user = request.user
                cart.save()
        else:
            new_obj = True
            cart = self.new(request.user)
        request.session["cart_id"] = cart.id

        return cart, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(max_digits=30, decimal_places=2, default=0.00)
    sub_total = models.DecimalField(max_digits=30,
                                    decimal_places=2,
                                    default=0.00)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    @property
    def subtotal(self):
        return self.sub_total


def m2m_change_cart_recever(sender, instance, action, *args, **kwargs):
    if action == "post_add" or action == "post_remove" or action == "post_clear":
        products = instance.products.all()
        total = 0

        for product in products:
            total += product.price

        if instance.sub_total != total:
            instance.sub_total = total
            instance.save()


m2m_changed.connect(m2m_change_cart_recever, sender=Cart.products.through)


def pre_save_cart_recever(sender, instance, *args, **kwargs):
    if instance.sub_total > 0:
        instance.total = Decimal( instance.sub_total) * Decimal(1.08)  # 8% tax
    else:
        instance.total = 0.00


pre_save.connect(pre_save_cart_recever, sender=Cart)
