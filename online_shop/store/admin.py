from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (CartItem, MainCategory, Category, Product, ShoppingCart)


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
