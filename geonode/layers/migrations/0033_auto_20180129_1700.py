# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0032_auto_20180129_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='layer',
            name='abstract_en',
        ),
        migrations.RemoveField(
            model_name='layer',
            name='constraints_other_en',
        ),
        migrations.RemoveField(
            model_name='layer',
            name='data_quality_statement_en',
        ),
        migrations.RemoveField(
            model_name='layer',
            name='purpose_en',
        ),
        migrations.RemoveField(
            model_name='layer',
            name='supplemental_information_en',
        ),
        migrations.RemoveField(
            model_name='layer',
            name='title_en',
        ),
    ]
