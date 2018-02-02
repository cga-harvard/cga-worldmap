# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0030_auto_20171231_1912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='backup',
            old_name='description_en',
            new_name='description_zh_cn',
        ),
        migrations.RenameField(
            model_name='backup',
            old_name='name_en',
            new_name='name_zh_cn',
        ),
        migrations.RenameField(
            model_name='license',
            old_name='description_en',
            new_name='description_zh_cn',
        ),
        migrations.RenameField(
            model_name='license',
            old_name='license_text_en',
            new_name='license_text_zh_cn',
        ),
        migrations.RenameField(
            model_name='license',
            old_name='name_en',
            new_name='name_zh_cn',
        ),
        migrations.RenameField(
            model_name='region',
            old_name='name_en',
            new_name='name_zh_cn',
        ),
        migrations.RenameField(
            model_name='restrictioncodetype',
            old_name='description_en',
            new_name='description_zh_cn',
        ),
        migrations.RenameField(
            model_name='restrictioncodetype',
            old_name='gn_description_en',
            new_name='gn_description_zh_cn',
        ),
        migrations.RenameField(
            model_name='spatialrepresentationtype',
            old_name='description_en',
            new_name='description_zh_cn',
        ),
        migrations.RenameField(
            model_name='spatialrepresentationtype',
            old_name='gn_description_en',
            new_name='gn_description_zh_cn',
        ),
        migrations.RenameField(
            model_name='topiccategory',
            old_name='description_en',
            new_name='description_zh_cn',
        ),
        migrations.RenameField(
            model_name='topiccategory',
            old_name='gn_description_en',
            new_name='gn_description_zh_cn',
        ),
    ]
