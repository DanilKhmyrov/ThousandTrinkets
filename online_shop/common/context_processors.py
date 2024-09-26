from store.models import CartItem, MainCategory, ShoppingCart


def main_categories(request):
    main_categories = MainCategory.objects.prefetch_related(
        'categories').all().order_by('name')
    return {
        'main_categories': main_categories,
    }


def favorites_and_cart_count(request):
    if request.user.is_authenticated:
        try:
            shopping_cart = request.user.shopping_cart.get()
        except ShoppingCart.DoesNotExist:
            shopping_cart = None

        if shopping_cart:
            cart_items = CartItem.objects.filter(
                cart=shopping_cart).select_related('product')
            is_in_cart = [item.product for item in cart_items]
            cart_items_count = len(is_in_cart)
        else:
            is_in_cart = []
            cart_items_count = 0

        favorites_items = request.user.favorites.select_related(
            'category').all()
        is_favorites = [fav for fav in favorites_items]
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
