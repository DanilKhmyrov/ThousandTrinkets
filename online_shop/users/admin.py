from django.contrib import admin
from django.contrib.auth import get_user_model
from django.http import HttpRequest

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    def get_queryset(self, request: HttpRequest):
        qs = super().get_queryset(request)
        return qs.prefetch_related('favorites')

    exclude = ('favorites',)

    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'phone_number')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
