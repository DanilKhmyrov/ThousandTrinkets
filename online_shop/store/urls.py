from django.conf import settings
from django.urls import path, include
from .views import (IndexListView, CategoryListView,
                    ProductDetailView, MainCategoryListView,
                    SearchResultsView, ajax_search)

app_name = 'store'

urlpatterns = []

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

urlpatterns += [
    path('', IndexListView.as_view(), name='home'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('ajax-search/', ajax_search, name='ajax_search'),
    path('<str:main_category_slug>/',
         MainCategoryListView.as_view(), name='main_category'),
    path('<str:main_category_slug>/<str:category_slug>/',
         CategoryListView.as_view(), name='category'),
    path('<str:main_category_slug>/<str:category_slug>/<str:article_number>/',
         ProductDetailView.as_view(), name='product'),
]
