from http import HTTPStatus as hs

import pytest
from pytest_lazyfixture import lazy_fixture as lf

from users.tasks import create_order_task
from store.models import CartItem

pytestmark = pytest.mark.django_db


def test_user_can_toggle_favorite(
        user, auth_user_client, toggle_favorite_url):
    before_count = user.favorites.count()
    response = auth_user_client.post(toggle_favorite_url)
    after_count = user.favorites.count()
    assert response.status_code == hs.OK
    assert after_count == before_count + 1


def test_auth_user_have_shopping_cart(user):
    cart = user.shopping_cart.get()
    assert cart


def test_auth_user_can_update_shopping_cart(
        user, auth_user_client, update_cart_url, product):
    cart = user.shopping_cart.get()
    before_count = cart.items.count()
    response = auth_user_client.post(
        update_cart_url,
        data={'productId': product.id, 'quantity': 1})
    after_count = cart.items.count()
    assert response.status_code == hs.OK
    assert after_count == before_count + 1


def test_anon_user_cant_update_shopping_cart(
        client, update_cart_url, product):
    response = client.post(
        update_cart_url,
        data={'productId': product.id, 'quantity': 1})
    assert response.status_code == hs.FORBIDDEN


def test_auth_user_can_create_order(
        user_with_cart_items, auth_user_client_with_cart, order_checkout_url):
    before_count = user_with_cart_items.orders.count()
    response = auth_user_client_with_cart.post(order_checkout_url)
    create_order_task(user_with_cart_items.id)
    after_count = user_with_cart_items.orders.count()
    assert response.status_code == hs.FOUND
    assert after_count == before_count + 1
