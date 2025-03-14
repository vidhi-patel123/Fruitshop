# Generated by Django 4.2.1 on 2024-04-04 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_category_gallery'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(upload_to='img')),
                ('G_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.category_gallery')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.add_product')),
            ],
        ),
    ]
