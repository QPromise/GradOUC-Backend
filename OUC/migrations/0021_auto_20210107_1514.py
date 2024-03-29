# Generated by Django 2.2.6 on 2021-01-07 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OUC', '0020_auto_20201221_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribestudent',
            name='legal_subscribe_date',
            field=models.CharField(default='-', max_length=1024, verbose_name='每次订阅的时间戳（有效期七天以内）'),
        ),
        migrations.AlterField(
            model_name='subscribestudent',
            name='new_send_message',
            field=models.CharField(default='-', max_length=256, verbose_name='最新发送的成绩'),
        ),
        migrations.AlterField(
            model_name='subscribestudent',
            name='status',
            field=models.IntegerField(default=0, verbose_name='订阅次数(1及其以上为订阅，0为没有)'),
        ),
    ]
