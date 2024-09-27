from django.urls import path
from .views import (OrderListView, UserProfileView, UserFavoriteView,
                    UserShoppingCartView, checkout, toggle_favorite,
                    update_cart)

app_name = 'user'

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('favorites/', UserFavoriteView.as_view(), name='favorites'),
    path('shopping-cart/', UserShoppingCartView.as_view(), name='shopping-cart'),
    path('toggle-favorite/<slug:article>/',
         toggle_favorite, name='toggle_favorite'),
    path('update-cart/', update_cart, name='update_cart'),
    path('order/checkout/', checkout, name='order_checkout'),
    path('order/confirmation/', OrderListView.as_view(), name='order_confirmation'),
]
