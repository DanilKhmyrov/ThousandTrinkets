from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import MainCategory, Category, Product


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


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


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


admin.site.register(MainCategory, MainCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
