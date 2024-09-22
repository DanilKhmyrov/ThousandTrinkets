from django.urls import path
from .views import dashboard

app_name = 'custom_admin'

urlpatterns = [
    path('', dashboard, name='admin_dashboard'),
]
