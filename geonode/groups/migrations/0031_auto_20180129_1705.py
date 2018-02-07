# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0030_auto_20180129_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupcategory',
            name='name_en',
            field=models.CharField(max_length=255, unique=True, null=True),
        ),
        migrations.AddField(
            model_name='groupprofile',
            name='description_en',
            field=models.TextField(null=True, verbose_name='\u63cf\u8ff0'),
        ),
        migrations.AddField(
            model_name='groupprofile',
            name='title_en',
            field=models.CharField(max_length=50, null=True, verbose_name='\u6807\u9898'),
        ),
    ]
