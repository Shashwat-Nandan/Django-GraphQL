# Generated by Django 3.1.7 on 2021-02-23 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sku_size',
            field=models.CharField(max_length=100),
        ),
    ]
