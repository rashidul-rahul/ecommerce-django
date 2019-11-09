from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView
from .models import Product


class ProductFeaturedListView(ListView):
    queryset = Product.objects.all().featured()

    template_name = "product/products.html"
    context_object_name = "products"


class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.all().featured()
    template_name = "product/featured-product.html"


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "product/products.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    template_name = "product/product.html"
    context_object_name = "product"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(
            *args, **kwargs)
        print(context)
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get("slug")

        try:
            isinstance = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            raise Http404("Product Not found")
        except Product.MultipleObjectsReturned:
            isinstance = Product.objects.filter(slug=slug).first()
        except:
            raise "Unknown Error"
        return isinstance
