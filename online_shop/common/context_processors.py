from store.models import MainCategory


def main_categories(request):
    main_categories = MainCategory.objects.prefetch_related(
        'categories').all().order_by('name')
    return {
        'main_categories': main_categories,
    }
