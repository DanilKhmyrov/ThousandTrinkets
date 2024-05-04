from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class AboutTemplateView(TemplateView):
    template_name = 'pages/about.html'


def error_500(request):
    return render(request, 'pages/500.html', status=500)


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)
