# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0026_map_content_map'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='template_page',
            field=models.CharField(max_length=255, verbose_name=b'Map template page', blank=True),
        ),
    ]
