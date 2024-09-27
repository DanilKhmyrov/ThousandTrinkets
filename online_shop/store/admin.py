from .models import Order, OrderItem
from django.contrib import admin
from django.utils.safestring import mark_safe


from .models import (CartItem, MainCategory, Category,
                     Order, OrderItem, Product, ShoppingCart)


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image_tag', 'icon_class')
    readonly_fields = ('image_tag',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CategoryInline]
    list_editable = ('icon_class',)

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "Нет изображения"

    image_tag.short_description = 'Изображение'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'main_category', 'image_tag', 'icon_class')
    list_filter = ('main_category',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('main_category', 'icon_class')

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "Нет изображения"

    image_tag.short_description = 'Изображение'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'quantity', 'get_total_price')
    readonly_fields = ('get_total_price',)

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Общая стоимость товара'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_price', 'created_at', 'updated_at')
    inlines = [CartItemInline]

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Общая стоимость корзины'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'get_total_price')
    readonly_fields = ('get_total_price',)

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Общая стоимость товара'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'user', 'status', 'created_at',
                    'updated_at', 'get_total_order_price', 'get_order_items')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'status', 'id')
    readonly_fields = ('created_at', 'updated_at', 'get_total_order_price')

    list_editable = ('status',)

    def get_total_order_price(self, obj):
        return obj.get_total_price()
    get_total_order_price.short_description = 'Общая стоимость заказа'

    def get_order_items(self, obj):
        """
        Возвращает список товаров с количеством и ссылкой
        для отображения в столбик.
        """
        items = obj.items.all().select_related(
            'product', 'product__category__main_category')

        def generate_product_link(item):
            product = item.product
            if product.category and product.category.main_category:
                return (
                    f'<a href="{product.get_absolute_url()}">'
                    f'{product.name}</a> ({item.quantity} шт.)'
                )
            return f'{product.name} ({item.quantity} шт.)'
        return mark_safe('<br>'.join([generate_product_link(item) for item in items]))
    get_order_items.short_description = 'Товары в заказе'
