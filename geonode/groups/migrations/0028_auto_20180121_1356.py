# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0027_auto_20171231_1912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupcategory',
            old_name='name_en',
            new_name='name_zh_cn',
        ),
        migrations.RenameField(
            model_name='groupprofile',
            old_name='description_en',
            new_name='description_zh_cn',
        ),
        migrations.RenameField(
            model_name='groupprofile',
            old_name='title_en',
            new_name='title_zh_cn',
        ),
    ]
