# Generated by Django 3.1.6 on 2021-02-17 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='type',
        ),
        migrations.AddField(
            model_name='user',
            name='kind',
            field=models.CharField(choices=[('RETAILER', 'Retailer'), ('CUSTOMER', 'Customer')], default='RETAILER', max_length=50, verbose_name='Kind'),
        ),
    ]
