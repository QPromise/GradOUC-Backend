# Generated by Django 2.2.6 on 2022-01-22 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OUC', '0063_auto_20220123_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='extra',
            field=models.TextField(default='', null=True, verbose_name='其它信息'),
        ),
    ]