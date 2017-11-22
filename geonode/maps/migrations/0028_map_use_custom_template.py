# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0027_map_template_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='use_custom_template',
            field=models.BooleanField(default=False, verbose_name='Use a custom template'),
        ),
    ]
