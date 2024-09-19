from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from store.models import Product
from .utils import get_product_count_text

User = get_user_model()


@login_required
def toggle_favorite(request, article):
    user = request.user
    product = get_object_or_404(Product, article_number=article)

    if product in user.favorites.all():
        user.favorites.remove(product)
        is_favorite = False
    else:
        user.favorites.add(product)
        is_favorite = True
    return JsonResponse({'is_favorite': is_favorite})


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'store/user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['products'] = get_product_count_text(user.favorites.count())
        return context


class UserFavoriteView(DetailView):
    model = User
    template_name = 'store/user/favorite.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.object.favorites.all()
        return context
