from http import HTTPStatus as hs

import pytest
from pytest_lazyfixture import lazy_fixture as lf

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'reverse_url, user_client, expected_status',
    (
        (lf('main_category_url'), lf('auth_user_client'), hs.OK),
        (lf('category_url'), lf('auth_user_client'), hs.OK),
        (lf('product_url'), lf('auth_user_client'), hs.OK),
        (lf('about_url'), lf('auth_user_client'), hs.OK),
        (lf('homepage_url'), lf('auth_user_client'), hs.OK),
        (lf('serch_url'), lf('auth_user_client'), hs.OK),
        (lf('apply_promo_url'), lf('auth_user_client'), hs.METHOD_NOT_ALLOWED),
    )
)
def test_availability_for_url(
        user_client, expected_status, reverse_url):
    response = user_client.get(reverse_url)
    assert response.status_code == expected_status
