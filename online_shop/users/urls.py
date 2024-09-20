from django.urls import path
from .views import (UserProfileView, UserFavoriteView,
                    UserShoppingCartView, toggle_favorite,
                    update_cart)

app_name = 'user'

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('favorites/', UserFavoriteView.as_view(), name='favorites'),
    path('shopping-cart/', UserShoppingCartView.as_view(), name='shopping-cart'),
    path('toggle-favorite/<int:article>/',
         toggle_favorite, name='toggle_favorite'),
    path('update-cart/', update_cart, name='update_cart'),
]
