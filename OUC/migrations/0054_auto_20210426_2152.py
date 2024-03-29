# Generated by Django 2.2.6 on 2021-04-26 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OUC', '0053_auto_20210426_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='dreamoucprofession',
            name='profession_hot_val',
            field=models.IntegerField(default=390, max_length=10, verbose_name='专业热度'),
        ),
        migrations.AlterField(
            model_name='dreamoucprofession',
            name='open_course_title',
            field=models.CharField(default='免费高分学长/学姐经验分享公开课', max_length=20, verbose_name='公开课名称'),
        ),
        migrations.AlterField(
            model_name='dreamoucprofession',
            name='profession_material_title',
            field=models.CharField(default='资料内容介绍及备考经验', max_length=20, verbose_name='资料及经验名称(10个字左右)'),
        ),
    ]
