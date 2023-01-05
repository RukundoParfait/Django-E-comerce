from django.urls import path
from store.views import *


urlpatterns=[
    path('', home, name='home'),
    path('cart', cart, name='cart'),
    path('checkout', checkout, name='checkout'),
    path('<str:product_category>/<str:product_name>/<int:product_id>', product, name='product'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('update-cart', update_cart, name='update_cart'),
]