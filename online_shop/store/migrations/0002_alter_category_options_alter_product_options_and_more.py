# Generated by Django 4.2.11 on 2024-07-30 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=30, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='article_number',
            field=models.CharField(max_length=50, unique=True, verbose_name='Артикул'),
        ),
    ]
