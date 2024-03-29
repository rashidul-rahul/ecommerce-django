from django.db import models
from django.db.models.signals import pre_save, post_save

from products.models import Product
from ecommerce.utils import unique_slug_generator


class Tag(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.title


def tag_pre_save_recever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(tag_pre_save_recever, sender=Tag)
