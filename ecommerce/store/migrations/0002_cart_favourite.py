# Generated by Django 4.1.6 on 2023-02-26 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('abstractproductcontainer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.abstractproductcontainer')),
            ],
            options={
                'abstract': False,
            },
            bases=('store.abstractproductcontainer',),
        ),
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('abstractproductcontainer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.abstractproductcontainer')),
            ],
            options={
                'abstract': False,
            },
            bases=('store.abstractproductcontainer',),
        ),
    ]
