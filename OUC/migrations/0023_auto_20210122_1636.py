# Generated by Django 2.2.6 on 2021-01-22 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OUC', '0022_auto_20210122_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentrank',
            name='avg_score',
            field=models.FloatField(default=0, verbose_name='平均学分绩'),
        ),
    ]
