from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class MainCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    icon_class = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='main_category_images/',
                              blank=True, null=True, verbose_name='Изображение')

    def get_absolute_url(self):
        return reverse('store:main_category', args=[self.slug])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Общая категория'
        verbose_name_plural = 'Общие категории'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True)
    slug = models.SlugField(max_length=30, unique=True, blank=True, null=True)
    main_category = models.ForeignKey(
        MainCategory,
        related_name='categories',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    icon_class = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(
        upload_to='category_images/', blank=True, null=True, verbose_name='Изображение')

    def get_absolute_url(self):
        return reverse('store:category', args=[self.main_category.slug, self.slug])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    article_number = models.CharField(
        max_length=50, unique=True, verbose_name='Артикул')
    price = models.FloatField(
        max_length=15, blank=True, null=True, verbose_name='Цена')
    purchase_price = models.FloatField(
        max_length=15, blank=True, null=True, verbose_name='Закупочная цена')
    remains = models.FloatField(
        max_length=15, blank=True, null=True, verbose_name='Остаток')
    remains_cost = models.FloatField(
        max_length=15, blank=True, null=True, verbose_name='Стоимость остатка')
    retail_remains_cost = models.FloatField(
        max_length=15, blank=True, null=True,
        verbose_name='Закупочная стоимость остатка')
    percent = models.FloatField(
        max_length=15, blank=True, null=True, verbose_name='Процент')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='products',
        verbose_name='Категория')
    image = models.ImageField(
        upload_to='product_images/', blank=True, null=True, verbose_name='Изображение')

    def get_absolute_url(self):
        return reverse('store:product',
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
        related_name='shopping_cart')
    products = models.ManyToManyField(Product, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина {self.user.username}'

    class Meta:
        ordering = ('id',)

    def get_total_price(self):
        """Возвращает общую сумму товаров в корзине"""
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} в количестве {self.quantity}'

    def get_total_price(self):
        """Возвращает общую стоимость для данного товара в корзине"""
        return self.product.price * self.quantity
