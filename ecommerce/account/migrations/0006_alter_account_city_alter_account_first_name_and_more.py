# Generated by Django 4.1.6 on 2023-04-26 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_account_city_account_first_name_account_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='city',
            field=models.CharField(max_length=99),
        ),
        migrations.AlterField(
            model_name='account',
            name='first_name',
            field=models.CharField(max_length=99),
        ),
        migrations.AlterField(
            model_name='account',
            name='last_name',
            field=models.CharField(max_length=99),
        ),
        migrations.AlterField(
            model_name='account',
            name='postal_code',
            field=models.CharField(max_length=99),
        ),
        migrations.AlterField(
            model_name='account',
            name='state',
            field=models.CharField(max_length=99),
        ),
    ]