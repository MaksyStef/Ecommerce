# Generated by Django 4.1.6 on 2023-04-25 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_delete_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractOrderContainer',
            fields=[
                ('abstractcontainer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.abstractcontainer')),
            ],
            options={
                'abstract': False,
            },
            bases=('store.abstractcontainer',),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]
