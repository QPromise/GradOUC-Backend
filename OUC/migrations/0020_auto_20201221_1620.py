# Generated by Django 2.2.6 on 2020-12-21 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OUC', '0019_subscribestudent_failure_popup'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribestudent',
            name='new_send_message',
            field=models.CharField(default='-', max_length=256, verbose_name='最新发送的消息'),
        ),
        migrations.AlterField(
            model_name='subscribestudent',
            name='failure_popup',
            field=models.IntegerField(default=1, verbose_name='是否失效弹窗(1为失效弹窗，0为失效不弹窗)'),
        ),
        migrations.AlterField(
            model_name='subscribestudent',
            name='scores',
            field=models.CharField(default='-', max_length=256, verbose_name='成绩'),
        ),
    ]
