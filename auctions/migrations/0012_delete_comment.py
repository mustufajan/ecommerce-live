# Generated by Django 3.0.8 on 2020-07-28 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
