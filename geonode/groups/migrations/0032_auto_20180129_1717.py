# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0031_auto_20180129_1705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupcategory',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='groupprofile',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='groupprofile',
            name='title_en',
        ),
    ]
