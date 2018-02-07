# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0029_auto_20180129_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='map',
            name='abstract_en',
        ),
        migrations.RemoveField(
            model_name='map',
            name='constraints_other_en',
        ),
        migrations.RemoveField(
            model_name='map',
            name='data_quality_statement_en',
        ),
        migrations.RemoveField(
            model_name='map',
            name='purpose_en',
        ),
        migrations.RemoveField(
            model_name='map',
            name='supplemental_information_en',
        ),
        migrations.RemoveField(
            model_name='map',
            name='title_en',
        ),
    ]
