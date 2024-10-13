from decimal import Decimal
from django.db import models
from django.db.models import Sum, F
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class MainCategory(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField('Слаг', max_length=50, unique=True)
    icon_class = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(
        'Изображение', upload_to='main_category_images/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('store:main_category', args=[self.slug])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Общая категория'
        verbose_name_plural = 'Общие категории'


class Category(models.Model):
    name = models.CharField('Название', max_length=100, unique=True, null=True)
    slug = models.SlugField('Слаг', max_length=30,
                            unique=True, blank=True, null=True)
    main_category = models.ForeignKey(MainCategory, related_name='categories',
                                      on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Главная категория')
    icon_class = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(
        'Изображение', upload_to='category_images/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('store:category', args=[self.main_category.slug, self.slug])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField('Наименование', max_length=100)
    article_number = models.CharField('Артикул', max_length=50, unique=True)
    price = models.DecimalField(
        'Цена', max_digits=10, decimal_places=2, blank=True, null=True)
    purchase_price = models.DecimalField(
        'Закупочная цена', max_digits=10, decimal_places=2, blank=True, null=True)
    remains = models.DecimalField(
        'Остаток', max_digits=10, decimal_places=2, blank=True, null=True)
    remains_cost = models.DecimalField(
        'Стоимость остатка', max_digits=10, decimal_places=2, blank=True, null=True)
    retail_remains_cost = models.DecimalField(
        'Закупочная стоимость остатка', max_digits=10, decimal_places=2, blank=True, null=True)
    percent = models.DecimalField(
        'Процент', max_digits=5, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='products', verbose_name='Категория')
    image = models.ImageField(
        'Изображение', upload_to='product_images/', blank=True, null=True)
    rating = models.DecimalField(default=0, max_digits=3, decimal_places=2)

    def get_absolute_url(self):
        return reverse('store:product', args=[self.category.main_category.slug, self.category.slug, self.article_number])

    def update_rating(self):
        reviews = self.reviews.all()
        avg_rating = reviews.aggregate(models.Avg('rating'))[
            'rating__avg'] or Decimal('0')
        self.rating = avg_rating
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Review(models.Model):
    product = models.ForeignKey(
        Product, related_name='reviews', on_delete=models.CASCADE, verbose_name='Товар')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.PositiveIntegerField(
        'Рейтинг', choices=[(i, i) for i in range(1, 6)], default=5)
    comment = models.TextField('Отзыв')
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_rating()

    def __str__(self):
        return f'Оценка {self.rating} на {self.product.name} от {self.user.username}'

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class AbstractCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='%(class)s', verbose_name='Пользователь')
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлена', auto_now=True)

    class Meta:
        abstract = True

    def get_total_price(self):
        """Подсчитывает общую стоимость товаров в корзине/заказе."""
        return self.items.aggregate(total_price=Sum(F('price') * F('quantity')))['total_price'] or Decimal('0')


class AbstractCartItem(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField('Количество', default=1)
    price = models.DecimalField(
        'Цена', max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = self.product.price
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

    def get_total_price(self):
        """Возвращает общую стоимость товара (цена * количество)."""
        if self.price is None:
            return self.product.price * self.quantity
        return self.price * self.quantity


class ShoppingCart(AbstractCart):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shopping_cart', verbose_name='Пользователь')

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(AbstractCartItem):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE,
                             related_name='items', verbose_name='Корзина')

    def __str__(self):
        return f'{self.product.name} в количестве {self.quantity}'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class PromoCode(models.Model):
    code = models.CharField('Промокод', max_length=50, unique=True)
    discount = models.DecimalField('Скидка %', max_digits=5, decimal_places=2)
    expiration_date = models.DateTimeField('Срок истечения')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True, blank=True, verbose_name='Пользователь')
    max_usage = models.PositiveIntegerField(
        'Колличество промокодов', default=1)
    times_used = models.PositiveIntegerField(
        'Колличество использований', default=0)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
        ordering = ['-id']

    def is_valid(self, user=None):
        """Проверка валидности промокода"""
        if self.expiration_date <= timezone.now():
            return False
        if self.times_used >= self.max_usage:
            return False
        if self.user and self.user != user:
            return False
        return True

    def get_discount_amount(self, total_price):
        """Рассчитываем сумму скидки на основе процента"""
        total_price = Decimal(total_price)
        return total_price * (self.discount / Decimal('100'))

    def apply_code(self):
        """Увеличиваем счетчик использования промокода"""
        self.times_used += 1
        self.save()


class Order(AbstractCart):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='orders', verbose_name='Пользователь')
    status = models.CharField(max_length=20, choices=[
        ('awaiting_delivery', 'Ожидает вручения'),
        ('assembling', 'В сборке'),
        ('confirmed', 'Подтвержден'),
        ('received', 'Получен'),
        ('canceled', 'Отменен'),
        ('returned', 'Возвращен')
    ], default='confirmed')
    total_price = models.DecimalField(
        'Общая сумма заказа', max_digits=10, decimal_places=2)
    discount = models.DecimalField(
        'Скидка', max_digits=10, decimal_places=2, default=0)
    final_price = models.DecimalField(
        'Итоговая цена', max_digits=10, decimal_places=2)
    promo_code = models.CharField(
        'Промокод', max_length=50, blank=True, null=True)

    def __str__(self):
        return f'Заказ пользователя {self.user.username}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def apply_promo_code(self, promo_code):
        """Применение промокода для расчета скидки"""
        if promo_code and promo_code.is_valid(self.user):
            discount_amount = promo_code.get_discount_amount(self.total_price)
            self.discount = discount_amount
            self.final_price = self.total_price - discount_amount
            self.promo_code = promo_code.code
        else:
            self.final_price = self.total_price
        self.save()


class OrderItem(AbstractCartItem):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')

    def __str__(self):
        return f'{self.product.name} в количестве {self.quantity} для заказа {self.order.id}'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
