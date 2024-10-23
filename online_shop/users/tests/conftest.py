import pytest

from django.test.client import Client
from django.urls import reverse

from store.models import CartItem, Category, MainCategory, Order, Product, ShoppingCart


@pytest.fixture(autouse=True)
def enable_celery_eager(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True


@pytest.fixture  # FIXME: Проверить как создается юзер в джанго, переопределить этот метод, тк сейчас раюотает только через форму создание корзины
def user(django_user_model):
    user = django_user_model.objects.create_user(
        username='testuser', password='testpass'
    )
    ShoppingCart.objects.create(user=user)
    return user


@pytest.fixture
def user_with_cart_items(django_user_model, product):
    user = django_user_model.objects.create_user(
        username='testuser1', password='testpass123'
    )
    ShoppingCart.objects.create(user=user)
    cart = user.shopping_cart.get()
    cart_item, _ = CartItem.objects.get_or_create(
        cart=cart, product=product)
    cart_item.quantity = 1
    cart_item.save()
    return user


@pytest.fixture
def auth_user_client(user):
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def auth_user_client_with_cart(user_with_cart_items):
    client = Client()
    client.force_login(user_with_cart_items)
    return client


@pytest.fixture
def main_category():
    main_category = MainCategory.objects.create(
        name='Test main category',
        slug='test-main-category'
    )
    return main_category


@pytest.fixture
def category(main_category):
    category = Category.objects.create(
        name='Test category',
        slug='test-category',
        main_category=main_category
    )
    return category


@pytest.fixture
def product(category):
    return Product.objects.create(
        name='Test Product',
        article_number=1,
        category=category,
        price=100,
        purchase_price=80,
        remains=10,
        remains_cost=20,
        retail_remains_cost=15,
    )


@pytest.fixture
def main_category_url(main_category):
    return reverse(
        'store:main_category',
        args=[
            main_category.slug
        ]
    )


@pytest.fixture
def category_url(main_category, category):
    return reverse(
        'store:category',
        args=[
            main_category.slug,
            category.slug
        ]
    )


@pytest.fixture
def product_url(main_category, category, product):
    return reverse(
        'store:product',
        args=[
            main_category.slug,
            category.slug,
            product.article_number
        ]
    )


@pytest.fixture
def order(user):
    return Order.objects.create(
        user=user, final_price=100, total_price=100)


@pytest.fixture
def order_detail_url(order):
    return reverse('user:order-detail', args=[order.id])


@pytest.fixture
def order_checkout_url():
    return reverse('user:order_checkout')


@pytest.fixture
def toggle_favorite_url(product):
    return reverse('user:toggle_favorite', args=[product.article_number])


@pytest.fixture
def profile_url():
    return reverse('user:profile')


@pytest.fixture
def profile_me_url():
    return reverse('user:me')


@pytest.fixture
def profile_promo_codes_url():
    return reverse('user:promo-codes')


@pytest.fixture
def profile_favorites_url():
    return reverse('user:favorites')


@pytest.fixture
def profile_shopping_cart_url():
    return reverse('user:shopping-cart')


@pytest.fixture
def update_cart_url():
    return reverse('user:update_cart')


@pytest.fixture
def profile_order_url():
    return reverse('user:order_confirmation')
