
from django.conf.urls import url

from products.views import (ProductListView,
                            ProductDetailView
                            )

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name="list"),
    url(r'^product/(?P<slug>[\w-]+)/$', ProductDetailView.as_view(),
        name="details")
]