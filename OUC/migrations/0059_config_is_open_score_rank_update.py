# Generated by Django 2.2.6 on 2021-10-10 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OUC', '0058_auto_20210428_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='is_open_score_rank_update',
            field=models.IntegerField(default=1, verbose_name='是否开启成绩排名的成绩更新(0:不开启,1:开启,2:只开启管理员的)'),
        ),
    ]