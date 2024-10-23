import pytest

from django.test.client import Client
from django.urls import reverse

from store.models import Category, MainCategory, Product


@pytest.fixture
def about_url():
    return reverse('pages:about')


@pytest.fixture
def homepage_url():
    return reverse('store:home')


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='testuser', password='testpass'
    )


@pytest.fixture
def auth_user_client(user):
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def logout():
    reverse('logout')


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
        category=category
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
def serch_url():
    return reverse('store:search_results')


@pytest.fixture
def apply_promo_url():
    return reverse('store:apply_promo_code')
