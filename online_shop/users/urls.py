from django.urls import path
from .views import UserProfileView, UserFavoriteView, toggle_favorite

app_name = 'user'

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('favorites/', UserFavoriteView.as_view(), name='favorites'),
    path('toggle-favorite/<int:article>/',
         toggle_favorite, name='toggle_favorite'),
]
