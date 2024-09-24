from store.models import MainCategory


def main_categories(request):
    main_categories = MainCategory.objects.prefetch_related(
        'categories').all().order_by('name')
    return {
        'main_categories': main_categories,
    }


def favorites_and_cart_count(request):
    if request.user.is_authenticated:
        cart_items = request.user.shopping_cart.items.select_related('product').all()
        favorites_items = request.user.favorites.select_related('category').all()

        is_in_cart = [item.product for item in cart_items]
        is_favorites = [fav for fav in favorites_items]
        cart_items_count = len(is_in_cart)
        favorites_count = len(is_favorites)
    else:
        favorites_count = 0
        cart_items_count = 0
        is_in_cart = []
        is_favorites = []

    return {
        'favorites_count': favorites_count,
        'cart_items_count': cart_items_count,
        'is_in_cart': is_in_cart,
        'is_favorites': is_favorites,
    }
