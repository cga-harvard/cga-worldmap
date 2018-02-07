# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0029_auto_20171107_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='attribute',
            field=models.CharField(help_text='\u5728shapefile\u548c\u7a7a\u95f4\u6570\u636e\u5e93\u4e2d\u4f7f\u7528\u7684\u5c5e\u6027\u540d\u79f0', max_length=255, null=True, verbose_name='\u5c5e\u6027\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='attribute_label',
            field=models.CharField(help_text='GeoNode\u4e2d\u663e\u793a\u5c5e\u6027\u7684\u6807\u9898', max_length=255, null=True, verbose_name='\u5c5e\u6027\u6807\u7b7e', blank=True),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='attribute_type',
            field=models.CharField(default=b'xsd:string', help_text='\u5c5e\u6027\u7684\u6570\u636e\u79cd\u7c7b(\u6574\u6570\uff0c\u5b57\u7b26\u4e32\uff0c\u51e0\u4f55\u56fe\u5f62\u7b49)', max_length=50, verbose_name='\u5c5e\u6027\u79cd\u7c7b'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='average',
            field=models.CharField(default=b'NA', max_length=255, null=True, verbose_name='\u5e73\u5747\u503c', help_text='\u6b64\u5217\u5e73\u5747\u503c'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='count',
            field=models.IntegerField(default=1, help_text='\u8ba1\u7b97\u6b64\u5217\u7684\u503c', verbose_name='\u6570\u76ee'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='date_format',
            field=models.CharField(max_length=255, null=True, verbose_name='\u65e5\u671f\u683c\u5f0f', blank=True),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='description',
            field=models.CharField(help_text='\u5728\u5143\u6570\u636e\u4e2d\u6240\u7528\u7684\u5c5e\u6027\u7684\u63cf\u8ff0', max_length=255, null=True, verbose_name='\u5c5e\u6027\u8bf4\u660e', blank=True),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='display_order',
            field=models.IntegerField(default=1, help_text='\u6807\u660e\u5c5e\u6027\u5728identity\u4e2d\u663e\u793a\u7684\u987a\u5e8f', verbose_name='\u663e\u793a\u987a\u5e8f'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='last_stats_updated',
            field=models.DateTimeField(default=datetime.datetime.now, help_text='\u4e0a\u4e00\u6b21\u7edf\u8ba1\u66f4\u65b0\u7684\u65f6\u95f4', verbose_name='\u6700\u540e\u4fee\u6539'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='max',
            field=models.CharField(default=b'NA', max_length=255, null=True, verbose_name='\u6700\u5927\u503c', help_text='\u6b64\u5217\u6700\u5927\u503c'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='median',
            field=models.CharField(default=b'NA', max_length=255, null=True, verbose_name='\u4e2d\u95f4\u503c', help_text='\u6b64\u5217\u4e2d\u95f4\u503c'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='min',
            field=models.CharField(default=b'NA', max_length=255, null=True, verbose_name='\u6700\u5c0f\u503c', help_text='\u6b64\u5217\u6700\u5c0f\u503c'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='stddev',
            field=models.CharField(default=b'NA', max_length=255, null=True, verbose_name='\u65b9\u5dee', help_text='\u6b64\u5217\u65b9\u5dee'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='sum',
            field=models.CharField(default=b'NA', max_length=255, null=True, verbose_name='\u548c', help_text='\u6b64\u5217\u548c'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='unique_values',
            field=models.TextField(default=b'NA', null=True, verbose_name='\u6b64\u5217\u552f\u4e00\u503c', blank=True),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='visible',
            field=models.BooleanField(default=True, help_text='\u6807\u660e\u662f\u5426\u5728identity\u4e2d\u663e\u793a\u5c5e\u6027', verbose_name='\u53ef\u89c1\uff1f'),
        ),
        migrations.AlterField(
            model_name='layer',
            name='abstract_en',
            field=models.TextField(help_text='\u8d44\u6599\u7b80\u4ecb', max_length=2000, null=True, verbose_name='\u6458\u8981', blank=True),
        ),
        migrations.AlterField(
            model_name='layer',
            name='constraints_other_en',
            field=models.TextField(help_text='\u4f7f\u7528\u8d44\u6599\u6216\u5143\u6570\u636e\u7684\u9650\u5236\u53ca\u6cd5\u5f8b\u524d\u63d0', null=True, verbose_name='\u5176\u4ed6\u9650\u5236', blank=True),
        ),
        migrations.AlterField(
            model_name='layer',
            name='data_quality_statement_en',
            field=models.TextField(help_text='\u5bf9\u4e8e\u6570\u636e\u96c6\u6cbf\u88ad\u7684\u57fa\u672c\u77e5\u8bc6', max_length=2000, null=True, verbose_name='\u6570\u636e\u8d28\u91cf\u63cf\u8ff0', blank=True),
        ),
        migrations.AlterField(
            model_name='layer',
            name='purpose_en',
            field=models.TextField(help_text='\u603b\u7ed3\u751f\u6210\u8d44\u6e90\u7684\u52a8\u673a', max_length=500, null=True, verbose_name='\u76ee\u6807', blank=True),
        ),
        migrations.AlterField(
            model_name='layer',
            name='supplemental_information_en',
            field=models.TextField(default='\u65e0\u4fe1\u606f\u63d0\u4f9b', max_length=2000, null=True, verbose_name='\u8865\u5145\u4fe1\u606f', help_text='\u5176\u4ed6\u5173\u4e8e\u6570\u636e\u7684\u63cf\u8ff0\u6027\u4fe1\u606f'),
        ),
        migrations.AlterField(
            model_name='layer',
            name='title_en',
            field=models.CharField(help_text='\u7528\u5df2\u77e5\u8d44\u6e90\u547d\u540d', max_length=255, null=True, verbose_name='\u6807\u9898'),
        ),
        migrations.AlterField(
            model_name='style',
            name='name',
            field=models.CharField(unique=True, max_length=255, verbose_name='\u683c\u5f0f\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='style',
            name='sld_body',
            field=models.TextField(null=True, verbose_name='sld\u6587\u672c', blank=True),
        ),
        migrations.AlterField(
            model_name='style',
            name='sld_url',
            field=models.CharField(max_length=1000, null=True, verbose_name='sld\u94fe\u63a5'),
        ),
        migrations.AlterField(
            model_name='style',
            name='sld_version',
            field=models.CharField(max_length=12, null=True, verbose_name='sld\u7248\u672c', blank=True),
        ),
    ]
