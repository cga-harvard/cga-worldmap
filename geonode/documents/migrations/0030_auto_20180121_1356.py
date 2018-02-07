# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0029_auto_20171231_1912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='abstract_en',
            new_name='abstract_zh_cn',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='constraints_other_en',
            new_name='constraints_other_zh_cn',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='data_quality_statement_en',
            new_name='data_quality_statement_zh_cn',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='purpose_en',
            new_name='purpose_zh_cn',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='supplemental_information_en',
            new_name='supplemental_information_zh_cn',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='title_en',
            new_name='title_zh_cn',
        ),
    ]
