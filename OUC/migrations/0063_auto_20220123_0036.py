# Generated by Django 2.2.6 on 2022-01-22 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OUC', '0062_auto_20220123_0035'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='studentinfo',
            name='idx_sno',
        ),
    ]