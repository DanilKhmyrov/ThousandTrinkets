from celery import shared_task
from .models import Order, ShoppingCart, OrderItem


@shared_task
def create_order_task(user_id):
    """Создает заказ для пользователя на основе его корзины."""
    try:
        cart = ShoppingCart.objects.get(user_id=user_id)
        if cart.items.exists():
            order = Order.objects.create(user_id=user_id)

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
            cart.items.all().delete()

            return f'Заказ {order.id} для {user_id} создан'

    except ShoppingCart.DoesNotExist:
        return f'Корзина пользователя {user_id} не найдена'
