# Generated by Django 5.1.4 on 2024-12-04 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bouquets', '0002_bouquet_created_at_alter_bouquet_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bouquet',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
