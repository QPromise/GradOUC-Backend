# Generated by Django 2.2.6 on 2020-01-07 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OUC', '0005_auto_20191120_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swiper',
            name='image',
            field=models.ImageField(upload_to='./static/upload_image/'),
        ),
    ]
