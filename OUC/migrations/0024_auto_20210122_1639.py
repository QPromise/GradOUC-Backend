# Generated by Django 2.2.6 on 2021-01-22 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OUC', '0023_auto_20210122_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentrank',
            name='avg_score',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=7, verbose_name='平均学分绩'),
        ),
    ]
