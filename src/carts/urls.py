from django.conf.urls import url

from carts.views import cart_home, cart_update, cart_checkout


urlpatterns = [
    url(r'^$', cart_home, name="home"),
    url(r'^update/$', cart_update, name="update"),
    url(r'^checkout/$', cart_checkout, name="checkout")
]
