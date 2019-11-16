import math
from django.db import models
from django.db.models.signals import pre_save, post_save

from ecommerce.utils import unique_order_id_generator

from carts.models import Cart


ORDER_STATUS_CHOICE = (
    ("created", "Created"),
    ("paid", "Paid"),
    ("shipped", "Shipped"),
    ("refunded", "Refunded"),
    ("cancelled", "Cancelled"),
)


class OrderManager(models.Manager):
    def get_or_new(self, cart):
        print(cart)
        qs = self.get_queryset().filter(cart=cart)
        if qs.count() == 1:
            order = qs.first()
            is_new = False
        else:
            order = self.new(cart)
            is_new = True

        return order, is_new

    def new(self, cart):
        return self.model.objects.create(cart=cart)


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    cart = models.ForeignKey(Cart)
    # billing_profile
    # shipping_address = models.CharField(max_length=200)
    # billing_address
    shipping_total = models.DecimalField(decimal_places=2,
                                         max_digits=50, default=9.99)
    total = models.DecimalField(decimal_places=2,
                                max_digits=50, default=9.99)
    status = models.CharField(max_length=120, default="created",
                              choices=ORDER_STATUS_CHOICE)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shippint_total = self.shipping_total
        total = math.fsum([cart_total, shippint_total])
        self.total = format(total, "2f")
        self.save()
        return total


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_order_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id

        qs = Order.objects.filter(cart__id=cart_id)

        if qs.count() == 1:
            order = qs.first()
            order.update_total()


post_save.connect(post_save_order_total, sender=Cart)


def post_save_update_total(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()


post_save.connect(post_save_update_total, sender=Order)
