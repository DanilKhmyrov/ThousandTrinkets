from store.models import MainCategory


def main_categories(request):
    main_categories = MainCategory.objects.prefetch_related(
        'categories').all().order_by('name')
    return {
        'main_categories': main_categories,
    }


def favorites_and_cart_count(request):
    if request.user.is_authenticated:
        favorites_count = request.user.favorites.count()
        cart_items_count = request.user.shopping_cart.items.count()
    else:
        favorites_count = 0
        cart_items_count = 0

    return {
        'favorites_count': favorites_count,
        'cart_items_count': cart_items_count,
    }
