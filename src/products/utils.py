import random
import string
from django.utils.text import slugify


def generate_rand_string(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assume model field have slug filed and
    title charfield
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    klass = instance.__class__
    qs_exists = klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=generate_rand_string(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    else:
        return slug
