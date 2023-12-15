# Generated by Django 4.1.1 on 2023-12-15 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_module', '0002_alter_watchlist_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cryptocompare_id', models.CharField(max_length=255, unique=True)),
                ('cryptocompare_symbol', models.CharField(max_length=255)),
                ('cryptocompare_coinname', models.CharField(max_length=255)),
                ('cryptocompare_fullname', models.CharField(max_length=255)),
                ('coingecko_id', models.CharField(max_length=255)),
                ('coingecko_symbol', models.CharField(max_length=255)),
                ('coingecko_name', models.CharField(max_length=255)),
                ('cryptocompare_imageurl', models.CharField(max_length=255)),
                ('cryptocompare_assetlaunchdate', models.CharField(max_length=255)),
                ('cryptocompare_assetwebsiteurl', models.CharField(max_length=255)),
                ('coin_status', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TokenOHLCV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=255)),
                ('currency', models.CharField(max_length=255)),
                ('open_value', models.CharField(max_length=255)),
                ('high', models.CharField(max_length=255)),
                ('low', models.CharField(max_length=255)),
                ('close_value', models.CharField(max_length=255)),
                ('volumefrom', models.CharField(max_length=255)),
                ('volumeto', models.CharField(max_length=255)),
                ('token', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_module.token')),
            ],
        ),
    ]
