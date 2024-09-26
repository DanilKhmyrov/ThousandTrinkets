from django.contrib import admin
from django.conf import settings
from django.views.generic.edit import CreateView
from django.conf.urls.static import static
from django.urls import path, include, reverse_lazy

from users.forms import RegistrationUserForm


urlpatterns = [
    path('admin/dashboard/', include('admin_panel.urls', namespace='custom_admin')),
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path('user/', include('users.urls', namespace='user')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=RegistrationUserForm,
            success_url=reverse_lazy('store:home')
        ),
        name='registration'
    ),
    path('', include('store.urls', namespace='store')),
]

handler500 = 'pages.views.error_500'
handler404 = 'pages.views.page_not_found'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
