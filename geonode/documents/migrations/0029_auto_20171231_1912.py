# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0028_auto_20170801_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='abstract_en',
            field=models.TextField(help_text='\u8d44\u6599\u7b80\u4ecb', max_length=2000, null=True, verbose_name='\u6458\u8981', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='constraints_other_en',
            field=models.TextField(help_text='\u4f7f\u7528\u8d44\u6599\u6216\u5143\u6570\u636e\u7684\u9650\u5236\u53ca\u6cd5\u5f8b\u524d\u63d0', null=True, verbose_name='\u5176\u4ed6\u9650\u5236', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='data_quality_statement_en',
            field=models.TextField(help_text='\u5bf9\u4e8e\u6570\u636e\u96c6\u6cbf\u88ad\u7684\u57fa\u672c\u77e5\u8bc6', max_length=2000, null=True, verbose_name='\u6570\u636e\u8d28\u91cf\u63cf\u8ff0', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='doc_file',
            field=models.FileField(max_length=255, upload_to=b'documents', null=True, verbose_name='\u6587\u4ef6', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='doc_url',
            field=models.URLField(help_text='\u7684\u6587\u6863\u7684URL\uff0c\u5982\u679c\u5b83\u662f\u5916\u90e8\u7684\u3002', max_length=255, null=True, verbose_name='\u7f51\u5740', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='purpose_en',
            field=models.TextField(help_text='\u603b\u7ed3\u751f\u6210\u8d44\u6e90\u7684\u52a8\u673a', max_length=500, null=True, verbose_name='\u76ee\u6807', blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='supplemental_information_en',
            field=models.TextField(default='\u65e0\u4fe1\u606f\u63d0\u4f9b', max_length=2000, null=True, verbose_name='\u8865\u5145\u4fe1\u606f', help_text='\u5176\u4ed6\u5173\u4e8e\u6570\u636e\u7684\u63cf\u8ff0\u6027\u4fe1\u606f'),
        ),
        migrations.AlterField(
            model_name='document',
            name='title_en',
            field=models.CharField(help_text='\u7528\u5df2\u77e5\u8d44\u6e90\u547d\u540d', max_length=255, null=True, verbose_name='\u6807\u9898'),
        ),
    ]
