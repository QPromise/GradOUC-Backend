# Generated by Django 2.2.6 on 2021-01-22 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OUC', '0030_auto_20210122_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentrank',
            name='avg_score',
            field=models.CharField(max_length=10, verbose_name='平均学分绩'),
        ),
    ]
