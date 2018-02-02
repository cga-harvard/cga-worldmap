# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0033_auto_20180129_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='backup',
            name='description_en',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='backup',
            name='name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='license',
            name='description_en',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='license',
            name='license_text_en',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='license',
            name='name_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='region',
            name='name_en',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='restrictioncodetype',
            name='description_en',
            field=models.TextField(max_length=255, null=True, editable=False),
        ),
        migrations.AddField(
            model_name='restrictioncodetype',
            name='gn_description_en',
            field=models.TextField(max_length=255, null=True, verbose_name=b'GeoNode description'),
        ),
        migrations.AddField(
            model_name='spatialrepresentationtype',
            name='description_en',
            field=models.CharField(max_length=255, null=True, editable=False),
        ),
        migrations.AddField(
            model_name='spatialrepresentationtype',
            name='gn_description_en',
            field=models.CharField(max_length=255, null=True, verbose_name=b'GeoNode description'),
        ),
        migrations.AddField(
            model_name='topiccategory',
            name='description_en',
            field=models.TextField(default=b'', null=True),
        ),
        migrations.AddField(
            model_name='topiccategory',
            name='gn_description_en',
            field=models.TextField(default=b'', null=True, verbose_name=b'GeoNode description'),
        ),
    ]
