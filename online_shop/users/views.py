from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from store.models import Product, CartItem, ShoppingCart
from .utils import get_product_count_text

User = get_user_model()


@login_required
@require_POST
def update_cart(request):
    """Обработка изменения количества товаров в корзине через AJAX."""
    product_id = request.POST.get('productId')
    quantity = request.POST.get('quantity')

    try:
        quantity = int(quantity)
    except ValueError:
        return JsonResponse({'error': 'Некорректное количество'}, status=400)
    # FIXME: настроить user.is_authenticated
    user = request.user

    cart, created = ShoppingCart.objects.get_or_create(user=user)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Товар не найден'}, status=404)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product)

    if quantity == 0:
        cart_item.delete()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    total_items = cart.items.count()
    total_price = cart.get_total_price()

    return JsonResponse({
        'total_items': total_items,
        'total_price': total_price,
        'item_quantity': cart_item.quantity if quantity > 0 else 0
    })


@login_required
def toggle_favorite(request, article):
    user = request.user
    product = get_object_or_404(Product, article_number=article)

    if product in user.favorites.all():
        user.favorites.remove(product)
        is_favorite = False
    else:
        user.favorites.add(product)
        is_favorite = True
    return JsonResponse({'is_favorite': is_favorite})


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'store/user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['products'] = get_product_count_text(user.favorites.count())
        context['cart_items_count'] = get_product_count_text(
            CartItem.objects.filter(cart=user.shopping_cart.get()).count())
        return context


class UserFavoriteView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'store/user/favorite.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # FIXME: Доделать product.is_in_cart в контекстный процессор
        context['products'] = self.object.favorites.all()
        return context


class UserShoppingCartView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'store/user/shopping_cart.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shopping_cart = self.object.shopping_cart.get()
        context['cart_items'] = CartItem.objects.filter(
            cart=shopping_cart).select_related('product')
        context['total_price'] = shopping_cart.get_total_price()
        return context
