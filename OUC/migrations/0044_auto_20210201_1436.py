# Generated by Django 2.2.6 on 2021-02-01 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OUC', '0043_auto_20210201_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swiper',
            name='image',
            field=models.ImageField(upload_to='./OUC/static/upload_image/'),
        ),
    ]