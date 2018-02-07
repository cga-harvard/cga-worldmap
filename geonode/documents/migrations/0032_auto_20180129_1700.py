# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0031_auto_20180129_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='abstract_en',
        ),
        migrations.RemoveField(
            model_name='document',
            name='constraints_other_en',
        ),
        migrations.RemoveField(
            model_name='document',
            name='data_quality_statement_en',
        ),
        migrations.RemoveField(
            model_name='document',
            name='purpose_en',
        ),
        migrations.RemoveField(
            model_name='document',
            name='supplemental_information_en',
        ),
        migrations.RemoveField(
            model_name='document',
            name='title_en',
        ),
    ]
