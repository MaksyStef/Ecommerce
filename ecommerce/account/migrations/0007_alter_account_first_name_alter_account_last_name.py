# Generated by Django 4.1.6 on 2023-04-26 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_account_city_alter_account_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='first_name',
            field=models.CharField(max_length=99, unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='last_name',
            field=models.CharField(max_length=99, unique=True),
        ),
    ]
