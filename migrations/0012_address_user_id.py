# Generated by Django 4.2.1 on 2024-03-22 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_add_to_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='user_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
