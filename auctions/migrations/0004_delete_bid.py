# Generated by Django 3.0.8 on 2020-07-20 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_bid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bid',
        ),
    ]