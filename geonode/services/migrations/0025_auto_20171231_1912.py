# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '24_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='method',
            field=models.CharField(max_length=1, choices=[(b'L', '\u5f53\u5730'), (b'C', '\u7ea7\u8054'), (b'H', '\u6536\u83b7'), (b'I', '\u7d22\u5f15'), (b'X', '\u76f4\u64ad'), (b'O', 'OpenGeoPortal')]),
        ),
        migrations.AlterField(
            model_name='service',
            name='type',
            field=models.CharField(max_length=4, choices=[(b'AUTO', '\u81ea\u52a8\u68c0\u6d4b'), (b'OWS', '\u914d\u5bf9WMS / WFS / WCS'), (b'WMS', '\u7f51\u7edc\u5730\u56fe\u670d\u52a1'), (b'CSW', '\u76ee\u5f55\u670d\u52a1'), (b'REST', 'ArcGIS\u7684REST\u670d\u52a1'), (b'OGP', 'OpenGeoPortal'), (b'HGL', '\u54c8\u4f5b\u5730\u7406\u7a7a\u95f4\u5e93')]),
        ),
        migrations.AlterField(
            model_name='servicelayer',
            name='description',
            field=models.TextField(null=True, verbose_name='\u5c42\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='servicelayer',
            name='styles',
            field=models.TextField(null=True, verbose_name='\u56fe\u5c42\u6837\u5f0f'),
        ),
        migrations.AlterField(
            model_name='servicelayer',
            name='title',
            field=models.CharField(max_length=512, verbose_name='\u5c42\u6807\u9898'),
        ),
        migrations.AlterField(
            model_name='servicelayer',
            name='typename',
            field=models.CharField(max_length=255, verbose_name='\u56fe\u5c42\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='serviceprofilerole',
            name='role',
            field=models.CharField(help_text='\u8d23\u4efb\u65b9\u5c65\u884c\u804c\u52a1', max_length=255, choices=[(b'author', '\u8d44\u6e90\u6388\u6743\u65b9'), (b'processor', '\u8d44\u6e90\u4fee\u6539\u65b9'), (b'publisher', '\u8d44\u6e90\u53d1\u5e03\u65b9'), (b'custodian', '\u63a5\u53d7\u95ee\u8d23\u548c\u8d23\u4efb\u7684\u6570\u636e\uff0c\u5e76\u786e\u4fdd\u8d44\u6e90\u7684\u9002\u5f53\u7684\u7ef4\u62a4\u548c\u4fdd\u517b\u65b9'), (b'pointOfContact', '\u8d44\u6e90\u4fe1\u606f\u67e5\u8be2\u65b9'), (b'distributor', '\u8d44\u6e90\u5206\u914d\u65b9'), (b'user', '\u8d44\u6e90\u4f7f\u7528\u65b9'), (b'resourceProvider', '\u8d44\u6e90\u63d0\u4f9b\u65b9'), (b'originator', '\u8d44\u6e90\u5236\u9020\u65b9'), (b'owner', '\u8d44\u6e90\u62e5\u6709\u65b9'), (b'principalInvestigator', '\u4fe1\u606f\u6536\u96c6\u4e0e\u7814\u7a76\u7684\u4e3b\u8981\u8d23\u4efb\u65b9')]),
        ),
        migrations.AlterField(
            model_name='webserviceregistrationjob',
            name='type',
            field=models.CharField(max_length=4, choices=[(b'AUTO', '\u81ea\u52a8\u68c0\u6d4b'), (b'OWS', '\u914d\u5bf9WMS / WFS / WCS'), (b'WMS', '\u7f51\u7edc\u5730\u56fe\u670d\u52a1'), (b'CSW', '\u76ee\u5f55\u670d\u52a1'), (b'REST', 'ArcGIS\u7684REST\u670d\u52a1'), (b'OGP', 'OpenGeoPortal'), (b'HGL', '\u54c8\u4f5b\u5730\u7406\u7a7a\u95f4\u5e93')]),
        ),
    ]
