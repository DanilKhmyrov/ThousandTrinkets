from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.AboutTemplateView.as_view(), name='about'),
]
