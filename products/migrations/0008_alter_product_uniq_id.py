# Generated by Django 4.1.6 on 2023-02-24 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_remove_product_variants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='uniq_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
