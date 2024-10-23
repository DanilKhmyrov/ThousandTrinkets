from http import HTTPStatus as hs

from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects
from django.test import Client
from pytest_lazyfixture import lazy_fixture as lf

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'reverse_url, user_client, expected_status',
    (
        (lf('profile_url'), lf('auth_user_client'), hs.OK),
        (lf('profile_me_url'), lf('auth_user_client'), hs.OK),
        (lf('profile_promo_codes_url'), lf('auth_user_client'), hs.OK),
        (lf('profile_favorites_url'), lf('auth_user_client'), hs.OK),
        (lf('profile_shopping_cart_url'), lf('auth_user_client'), hs.OK),
        (lf('profile_order_url'), lf('auth_user_client'), hs.OK),
        (lf('order_detail_url'), lf('auth_user_client'), hs.OK),
    )
)
def test_availability_for_auth_user_url(
        reverse_url, user_client, expected_status):
    response = user_client.get(reverse_url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'reverse_url, user_client, expected_status',
    (
        (lf('profile_url'), Client(), hs.FOUND),
        (lf('profile_me_url'), Client(), hs.FOUND),
        (lf('profile_promo_codes_url'), Client(), hs.FOUND),
        (lf('profile_favorites_url'), Client(), hs.FOUND),
        (lf('profile_shopping_cart_url'), Client(), hs.FOUND),
        (lf('profile_order_url'), Client(), hs.FOUND),
        (lf('order_detail_url'), Client(), hs.FOUND),
    )
)
def test_availability_for_anon_url(
        reverse_url, user_client, expected_status):
    login_url = reverse('login')
    redirect_url = f'{login_url}?next={reverse_url}'
    response = user_client.get(reverse_url)
    assert response.status_code == expected_status
    assertRedirects(response, redirect_url)
