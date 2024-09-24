from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class MainCategory(models.Model):
    name = models.CharField(
        'Название',
        max_length=100,
        unique=True)
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True)
    icon_class = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    image = models.ImageField(
        'Изображение',
        upload_to='main_category_images/',
        blank=True,
        null=True,)

    def get_absolute_url(self):
        return reverse('store:main_category', args=[self.slug])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Общая категория'
        verbose_name_plural = 'Общие категории'


class Category(models.Model):
    name = models.CharField(
        'Название',
        max_length=100,
        unique=True,
        null=True)
    slug = models.SlugField(
        'Слаг',
        max_length=30,
        unique=True,
        blank=True,
        null=True)
    main_category = models.ForeignKey(
        MainCategory,
        related_name='categories',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Главная категория')
    icon_class = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    image = models.ImageField(
        'Изображение',
        upload_to='category_images/',
        blank=True,
        null=True,)

    def get_absolute_url(self):
        return reverse('store:category', args=[self.main_category.slug, self.slug])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=100)
    article_number = models.CharField(
        'Артикул',
        max_length=50,
        unique=True)
    price = models.FloatField(
        'Цена',
        max_length=15,
        blank=True,
        null=True)
    purchase_price = models.FloatField(
        'Закупочная цена',
        max_length=15,
        blank=True,
        null=True)
    remains = models.FloatField(
        'Остаток',
        max_length=15,
        blank=True,
        null=True)
    remains_cost = models.FloatField(
        'Стоимость остатка',
        max_length=15,
        blank=True,
        null=True)
    retail_remains_cost = models.FloatField(
        'Закупочная стоимость остатка',
        max_length=15,
        blank=True,
        null=True)
    percent = models.FloatField(
        'Процент',
        max_length=15,
        blank=True,
        null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        verbose_name='Категория')
    image = models.ImageField(
        'Изображение',
        upload_to='product_images/',
        blank=True,
        null=True)

    def get_absolute_url(self):
        return reverse(
            'store:product',
            args=[self.category.main_category.slug,
                  self.category.slug,
                  self.article_number])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('id',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

# TODO: Добавить общую скидку на коризну каждому пользователю, которая зависит от суммы заказа


class ShoppingCart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь')
    products = models.ManyToManyField(
        Product,
        through='CartItem')
    created_at = models.DateTimeField(
        'Создана',
        auto_now_add=True)
    updated_at = models.DateTimeField(
        'Обновлено',
        auto_now_add=True)

    def __str__(self):
        return f'Корзина {self.user.username}'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def get_total_price(self):
        """Возвращает общую сумму товаров в корзине"""
        return self.items.aggregate(total_price=Sum('product__price'))['total_price'] or 0


class CartItem(models.Model):
    cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар')
    quantity = models.PositiveIntegerField(
        'Колличество',
        default=1)

    def __str__(self):
        return f'{self.product.name} в количестве {self.quantity}'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_total_price(self):
        """Возвращает общую стоимость для данного товара в корзине"""
        return self.product.price * self.quantity
