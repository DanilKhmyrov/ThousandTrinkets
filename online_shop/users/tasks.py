from datetime import timedelta

from django.utils import timezone
from celery import shared_task

from store.models import CartItem, Order, OrderItem, PromoCode, ShoppingCart


@shared_task
def create_order_task(user_id, promo_code=None):
    """Создает заказ для пользователя на основе его корзины и применяет промокод."""
    try:
        # Получаем корзину пользователя
        cart = ShoppingCart.objects.get(user_id=user_id)
        if cart.items.exists():
            # Рассчитываем полную сумму без учета скидок
            total_price = sum(item.product.price *
                              item.quantity for item in cart.items.all())

            # Создаем заказ
            order = Order.objects.create(
                user_id=user_id,
                total_price=total_price,
                final_price=total_price  # На случай если промокод не будет применен
            )

            # Применяем промокод, если он был передан, иначе метод apply_promo_code выполнит установку final_price
            promo = None
            if promo_code:
                promo = PromoCode.objects.get(code=promo_code)
                promo.apply_code()  # Теперь промокод считается использованным

            # Вызовем метод apply_promo_code всегда, с промокодом или без него
            order.apply_promo_code(promo)

            # Создаем элементы заказа
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                for item in cart.items.all()
            ]
            OrderItem.objects.bulk_create(order_items)

            # Очищаем корзину
            cart.items.all().delete()

            return f'Заказ {order.id} для пользователя {user_id} создан'

    except ShoppingCart.DoesNotExist:
        return f'Корзина пользователя {user_id} не найдена'


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def clear_old_shopping_cart(self):
    """Очищает корзины пользователей, измененные более 24 часов назад."""
    try:
        old_carts = ShoppingCart.objects.filter(
            updated_at__lte=timezone.now() - timedelta(hours=24)
        )
        CartItem.objects.filter(cart__in=old_carts).delete()
    except Exception as e:
        raise self.retry(exc=e)
