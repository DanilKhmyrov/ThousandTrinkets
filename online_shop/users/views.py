from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, UpdateView
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .forms import UserProfileForm
from .tasks import create_order_task
from store.models import Order, Product, CartItem, PromoCode, ShoppingCart
from .utils import get_product_count_text

User = get_user_model()


@login_required
@require_POST
# TODO: Добавить уведомление о новом заказе в админ панели
def checkout(request):
    user = request.user
    session = request.session
    promo_code = session.get('promo_code')
    with transaction.atomic():
        transaction.on_commit(lambda: create_order_task.delay(
            user.id, promo_code=promo_code))
    del request.session['promo_code']
    return redirect('user:order_confirmation')


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
    # FIXME: проверить почему не обновляется поле updated_at
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
    template_name = 'store/user/profile_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['products'] = get_product_count_text(user.favorites.count())
        context['named_cart_items_count'] = get_product_count_text(
            CartItem.objects.filter(cart=user.shopping_cart.get()).count())
        return context


class UserProfileMeView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'store/user/profile_me.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('user:profile')

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_invalid(self, form):
        # В случае ошибки, выводим уведомление об ошибке
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


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
        total_price = shopping_cart.get_total_price()
        promo_code = self.request.session.get('promo_code')
        discount = 0

        if promo_code:
            promo = PromoCode.objects.filter(code=promo_code).first()
            if promo and promo.is_valid(self.request.user):
                discount = promo.get_discount_amount(total_price)
                total_price -= discount

        context['total_price'] = round(total_price, 2)
        context['discount'] = round(discount, 2)
        context['promo_code_applied'] = promo_code

        return context


class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'store/user/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user = self.request.user
        return (
            Order.objects.filter(user=user)
            .prefetch_related('items__product')
            .prefetch_related('items__product__category')
            .select_related('user')
        )


class PromoCodeListView(LoginRequiredMixin, ListView):
    model = PromoCode
    template_name = 'store/user/profile_promo_code.html'
    context_object_name = 'promo_codes'

    def get_queryset(self):
        return PromoCode.objects.filter(
            Q(user=self.request.user) | Q(user__isnull=True)).select_related('user')
