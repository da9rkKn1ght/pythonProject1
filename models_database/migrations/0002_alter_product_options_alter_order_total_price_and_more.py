# Generated by Django 4.2.16 on 2024-10-26 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models_database', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['product_name'], 'verbose_name': ('Название продукта',), 'verbose_name_plural': ('Названия продуктов',)},
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Общая стоимость заказа'),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество'),
        ),
    ]
