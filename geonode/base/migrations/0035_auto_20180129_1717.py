# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0034_auto_20180129_1705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='backup',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='backup',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='license',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='license',
            name='license_text_en',
        ),
        migrations.RemoveField(
            model_name='license',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='region',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='restrictioncodetype',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='restrictioncodetype',
            name='gn_description_en',
        ),
        migrations.RemoveField(
            model_name='spatialrepresentationtype',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='spatialrepresentationtype',
            name='gn_description_en',
        ),
        migrations.RemoveField(
            model_name='topiccategory',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='topiccategory',
            name='gn_description_en',
        ),
    ]
