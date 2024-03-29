import random
import os

from django.urls import reverse
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from ecommerce.utils import unique_slug_generator


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(isinstance, filename):
    new_filename = random.randint(1, 3123143532)
    name, ext = get_filename_ext(filename)
    final_name = "{file_name}{ext}".format(file_name=new_filename, ext=ext)
    return "products/{}/{}".format(new_filename, final_name)


class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True)

    def active(self):
        return self.filter(active=True)

    def search(self, query):
        looksups = (Q(title__icontains=query)
                    | Q(description__icontains=query)
                    | Q(price__icontains=query)
                    | Q(tag__title__icontains=query)
                    )
        return self.filter(looksups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def featured(self):
        return self.get_queryset().featured()

    def is_active(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)  # product_objects = self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        else:
            return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=19, default=20.00)
    image = models.ImageField(upload_to=upload_image_path, null=True,
                              blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return "/products/product/{}".format(self.slug)
        return reverse("products:details", kwargs={"slug": self.slug})

    @property
    def name(self):
        return self.title


def product_pre_save_recever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance=instance)


pre_save.connect(product_pre_save_recever, sender=Product)
