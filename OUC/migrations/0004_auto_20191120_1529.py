# Generated by Django 2.2.6 on 2019-11-20 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OUC', '0003_swiper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swiper',
            name='url',
            field=models.CharField(max_length=500),
        ),
    ]
