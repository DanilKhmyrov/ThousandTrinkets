from django.urls import path
from .views import (
    OrderDetailView, PromoCodeListView,
    UpdateCartView, UserOrderListView,
    UserProfileMeView, UserProfileView,
    UserFavoriteView, UserShoppingCartView,
    checkout, toggle_favorite, )

app_name = 'user'

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/me/', UserProfileMeView.as_view(), name='me'),
    path('profile/me/promo-codes', PromoCodeListView.as_view(), name='promo-codes'),
    path('favorites/', UserFavoriteView.as_view(), name='favorites'),
    path('toggle-favorite/<slug:article>/',
         toggle_favorite, name='toggle_favorite'),
    path('shopping-cart/', UserShoppingCartView.as_view(), name='shopping-cart'),
    path('update-cart/', UpdateCartView.as_view(), name='update_cart'),
    path('order/checkout/', checkout, name='order_checkout'),
    path('order/confirmation/', UserOrderListView.as_view(),  # TODO: Изменить название ендпоинта
         name='order_confirmation'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order-detail')
]
