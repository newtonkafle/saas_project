# Generated by Django 5.0.9 on 2024-10-14 12:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0010_alter_subscriptionsprice_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriptions',
            options={'ordering': ['order', 'featured', '-updated'], 'permissions': [('advanced', 'Advanced Perm'), ('pro', 'Pro Perm'), ('basic', 'Basic Perm')]},
        ),
        migrations.AddField(
            model_name='subscriptions',
            name='featured',
            field=models.BooleanField(default=True, help_text='featured on Django pricing page'),
        ),
        migrations.AddField(
            model_name='subscriptions',
            name='order',
            field=models.IntegerField(default=-1, help_text='Ordering on django pricing page'),
        ),
        migrations.AddField(
            model_name='subscriptions',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscriptions',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
