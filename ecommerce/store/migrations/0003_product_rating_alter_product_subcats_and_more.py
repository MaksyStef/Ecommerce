# Generated by Django 4.1.6 on 2023-02-27 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_cart_favourite'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.PositiveIntegerField(blank=True, default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcats',
            field=models.ManyToManyField(blank=True, to='store.subcategory'),
        ),
        migrations.AlterField(
            model_name='product',
            name='votes',
            field=models.ManyToManyField(blank=True, to='store.vote'),
        ),
    ]
