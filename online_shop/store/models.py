from django.db import models
from django.urls import reverse

# Создайте здесь ваши модели.


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
        # Предполагаем, что URL-имя для продукта - 'product', и оно принимает слаг главной категории, слаг категории и артикул
        return reverse('store:product', args=[self.category.main_category.slug,
                                              self.category.slug,
                                              self.article_number])

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
