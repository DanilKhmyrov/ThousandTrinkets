# Generated by Django 4.2.11 on 2024-09-19 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_shoppingcart_created_at_shoppingcart_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.shoppingcart'),
        ),
    ]
