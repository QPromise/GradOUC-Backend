# Generated by Django 2.2.6 on 2021-02-01 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OUC', '0044_auto_20210201_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentrank',
            name='can_join_rank',
            field=models.IntegerField(default=1, verbose_name='是否可以参与排名(0:不及格或重修,1:正常)'),
        ),
    ]
