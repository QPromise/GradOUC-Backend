# Generated by Django 2.2.6 on 2021-01-22 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OUC', '0035_auto_20210122_1745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentrank',
            name='profession',
        ),
        migrations.RemoveField(
            model_name='studentrank',
            name='rank_profession',
        ),
        migrations.AddField(
            model_name='studentrank',
            name='rank_research',
            field=models.CharField(default='-', max_length=1024, verbose_name='参与排名的研究方向'),
        ),
        migrations.AddField(
            model_name='studentrank',
            name='research',
            field=models.CharField(default='-', max_length=40, verbose_name='研究方向'),
        ),
    ]