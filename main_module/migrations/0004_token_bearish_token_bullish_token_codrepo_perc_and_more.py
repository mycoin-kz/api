# Generated by Django 4.1.1 on 2023-12-17 18:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_module', '0003_token_tokenohlcv'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='bearish',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='token',
            name='bullish',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='token',
            name='codrepo_perc',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)]),
        ),
        migrations.AddField(
            model_name='token',
            name='fb_perc',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)]),
        ),
        migrations.AddField(
            model_name='token',
            name='fullname',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='token',
            name='imageurl',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='token',
            name='neutral',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='token',
            name='reddit_perc',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)]),
        ),
        migrations.AddField(
            model_name='token',
            name='symbol',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='token',
            name='total_perc',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)]),
        ),
        migrations.AddField(
            model_name='token',
            name='twitter_perc',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)]),
        ),
    ]