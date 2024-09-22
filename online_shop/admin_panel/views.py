from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count

from store.models import MainCategory, Product

User = get_user_model()


@staff_member_required
def dashboard(request):
    sales_datas = MainCategory.objects.annotate(
        product_count=Count('categories__products')
    )
    sales_data = [i.product_count for i in sales_datas]
    categories = [i.name for i in MainCategory.objects.all()]
    total_orders = Product.objects.count()
    total_visitors = User.objects.count()

    context = {
        "sales_data": sales_data,
        "categories": categories,
        "total_orders": total_orders,
        "total_visitors": total_visitors,
    }

    return render(request, 'admin/admin_dashboard.html', context)
