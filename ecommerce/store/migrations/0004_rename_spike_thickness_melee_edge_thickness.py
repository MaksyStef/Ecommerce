# Generated by Django 4.1.6 on 2023-03-01 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_rating_alter_product_subcats_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='melee',
            old_name='spike_thickness',
            new_name='edge_thickness',
        ),
    ]