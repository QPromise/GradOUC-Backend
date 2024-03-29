# Generated by Django 2.2.6 on 2021-02-09 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OUC', '0045_studentrank_can_join_rank'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sno', models.CharField(db_index=True, default='-', max_length=15, unique=True, verbose_name='学号')),
                ('name', models.CharField(db_index=True, default='-', max_length=15, verbose_name='姓名')),
                ('sex', models.CharField(default='-', max_length=5, verbose_name='性别')),
                ('date_of_birth', models.CharField(default='-', max_length=15, verbose_name='出生日期')),
                ('id_card', models.CharField(default='-', max_length=20, verbose_name='身份证号')),
                ('nation', models.CharField(default='-', max_length=20, verbose_name='民族')),
                ('id_info', models.CharField(default='-', max_length=20, verbose_name='个人信息')),
                ('hometown', models.CharField(default='-', max_length=100, verbose_name='籍贯')),
                ('start_year', models.CharField(default='-', max_length=4, verbose_name='年级')),
                ('study_period', models.CharField(default='-', max_length=10, verbose_name='学制')),
                ('degree_type', models.CharField(default='-', max_length=10, verbose_name='学位类别')),
                ('train_type', models.CharField(default='-', max_length=10, verbose_name='培养类型')),
                ('hukou_address', models.CharField(default='-', max_length=100, verbose_name='户口所在地')),
                ('home_tel', models.CharField(default='-', max_length=20, verbose_name='家庭电话')),
                ('home_postcode', models.CharField(default='-', max_length=10, verbose_name='家庭邮编')),
                ('home_detail', models.CharField(default='-', max_length=100, verbose_name='家庭地址')),
                ('come_from', models.CharField(default='-', max_length=50, verbose_name='来源')),
                ('file_unit', models.CharField(default='-', max_length=50, verbose_name='档案所在单位')),
                ('tel', models.CharField(default='-', max_length=20, verbose_name='电话')),
                ('department', models.CharField(db_index=True, default='-', max_length=20, verbose_name='学院')),
                ('profession', models.CharField(db_index=True, default='-', max_length=40, verbose_name='专业')),
                ('research', models.CharField(db_index=True, default='-', max_length=40, verbose_name='研究方向')),
            ],
        ),
    ]
