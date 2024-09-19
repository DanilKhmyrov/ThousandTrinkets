from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.http import HttpRequest

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    def get_queryset(self, request: HttpRequest):
        qs = super().get_queryset(request)
        return qs.prefetch_related('favorites')

    exclude = ('favorites',)  # Исключаем поле из формы

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active')