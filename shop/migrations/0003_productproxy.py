# Generated by Django 5.0.6 on 2024-07-18 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('shop.product',),
        ),
    ]
