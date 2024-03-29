# Generated by Django 4.1.6 on 2023-02-26 15:14

from django.db import migrations, models
import django.db.models.deletion
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_cart_favourite'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='cart',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.cart', verbose_name='Products in cart'),
        ),
        migrations.AddField(
            model_name='account',
            name='favourite',
            field=models.OneToOneField(default=store.models.Favourite.get_new, on_delete=django.db.models.deletion.CASCADE, to='store.favourite', verbose_name='Favourite products'),
        ),
    ]
