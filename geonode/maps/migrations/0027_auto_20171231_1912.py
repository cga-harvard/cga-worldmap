# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0026_map_content_map'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='abstract_en',
            field=models.TextField(help_text='\u8d44\u6599\u7b80\u4ecb', max_length=2000, null=True, verbose_name='\u6458\u8981', blank=True),
        ),
        migrations.AlterField(
            model_name='map',
            name='center_x',
            field=models.FloatField(verbose_name='\u4e2d\u5fc3X'),
        ),
        migrations.AlterField(
            model_name='map',
            name='center_y',
            field=models.FloatField(verbose_name='\u4e2d\u5fc3Y'),
        ),
        migrations.AlterField(
            model_name='map',
            name='constraints_other_en',
            field=models.TextField(help_text='\u4f7f\u7528\u8d44\u6599\u6216\u5143\u6570\u636e\u7684\u9650\u5236\u53ca\u6cd5\u5f8b\u524d\u63d0', null=True, verbose_name='\u5176\u4ed6\u9650\u5236', blank=True),
        ),
        migrations.AlterField(
            model_name='map',
            name='content_map',
            field=models.TextField(default='<h3>\u5173\u4e8e\u6211\u4eec</h3>  <p>\u707f\u70c2\u8f89\u714c\u7684\u4eba\u7c7b\u6587\u660e\u3001\u6d69\u5982\u70df\u6d77\u7684\u53e4\u4eca\u6587\u732e\u4ee5\u53ca\u5e7f\u88a4\u65e0\u57a0\u7684  \u9646\u5730\u6d77\u6d0b\uff0c\u5b58\u5728\u7740\u6d77\u91cf\u7684\u4e0e\u4eba\u7c7b\u6d3b\u52a8\u606f\u606f\u76f8\u5173\u7684\u5730\u7406\u4fe1\u606f\u3002  \u5c31\u5355\u4e2a\u4eba\u7269\u6765\u8bf4\uff0c\u5305\u62ec\u4eba\u7269\u7684\u7c4d\u8d2f\u3001\u884c\u8ff9\u3001\u793e\u4f1a\u5173\u7cfb\u7684\u5730\u7406\u5206\u5e03\uff1b  \u5c31\u7fa4\u4f53\u6765\u8bf4\uff0c\u5305\u62ec\u4e00\u4e2a\u7fa4\u4f53\u7684\u5730\u7406\u5206\u5e03\u548c\u8fc1\u5f99\u8f68\u8ff9\uff1b\u5c31\u975e\u751f\u547d  \u7684\u7269\u4f53\u6765\u8bf4\uff0c\u4e5f\u6709\u5176\u5b58\u5728\u3001\u5206\u5e03\u548c\u53d8\u5316\u7684\u5730\u7406\u533a\u57df\uff1b\u5c31\u4e00\u4e2a\u5730  \u65b9\u6765\u8bf4\uff0c\u5219\u53c8\u5305\u542b\u4e86\u65e2\u5f80\u65f6\u95f4\u91cc\u4eba\u3001\u4e8b\u3001\u7269\u7b49\u5730\u7406\u4fe1\u606f\u7684\u603b\u6c47\u3002</p>  <p>\u7531\u6d59\u6c5f\u5927\u5b66\u4e0e\u54c8\u4f5b\u5927\u5b66\u5171\u5efa\u7684\u5b66\u672f\u5730\u56fe\u53d1\u5e03\u5e73\u53f0\u613f\u4e3a\u5e7f\u5927  \u7528\u6237\u63d0\u4f9b\u5730\u7406\u4fe1\u606f\u7814\u7a76\u6210\u679c\u7684\u53d1\u5e03\u3001\u53ef\u89c6\u5316\u5206\u6790\u53ca\u591a\u529f\u80fd\u67e5  \u8be2\u670d\u52a1\uff0c\u5e73\u53f0\u6240\u5f62\u6210\u7684\u5927\u6570\u636e\uff0c\u53ef\u4ee5\u4e3a\u672a\u6765\u79d1\u5b66\u7814\u7a76\u3001\u653f\u5e9c\u51b3  \u7b56\u53ca\u793e\u4f1a\u670d\u52a1\u63d0\u4f9b\u91cd\u8981\u7684\u53c2\u8003\u3002</p>  <p style="text-align: right">\u6d59\u6c5f\u5927\u5b66\u5927\u6570\u636e\u4e0e\u4e2d\u56fd\u5b66\u672f\u5730\u56fe\u521b\u65b0\u56e2\u961f</p>  <p style="text-align: right">\u54c8\u4f5b\u5927\u5b66\u5730\u7406\u5206\u6790\u4e2d\u5fc3</p>  <p style="text-align: right"></p>', null=True, verbose_name='Site Content', blank=True),
        ),
        migrations.AlterField(
            model_name='map',
            name='data_quality_statement_en',
            field=models.TextField(help_text='\u5bf9\u4e8e\u6570\u636e\u96c6\u6cbf\u88ad\u7684\u57fa\u672c\u77e5\u8bc6', max_length=2000, null=True, verbose_name='\u6570\u636e\u8d28\u91cf\u63cf\u8ff0', blank=True),
        ),
        migrations.AlterField(
            model_name='map',
            name='featuredurl',
            field=models.CharField(max_length=255, verbose_name='\u7279\u8272\u5730\u56fe\u7f51\u5740', blank=True),
        ),
        migrations.AlterField(
            model_name='map',
            name='projection',
            field=models.CharField(max_length=32, verbose_name='\u6295\u5f71'),
        ),
        migrations.AlterField(
            model_name='map',
            name='purpose_en',
            field=models.TextField(help_text='\u603b\u7ed3\u751f\u6210\u8d44\u6e90\u7684\u52a8\u673a', max_length=500, null=True, verbose_name='\u76ee\u6807', blank=True),
        ),
        migrations.AlterField(
            model_name='map',
            name='supplemental_information_en',
            field=models.TextField(default='\u65e0\u4fe1\u606f\u63d0\u4f9b', max_length=2000, null=True, verbose_name='\u8865\u5145\u4fe1\u606f', help_text='\u5176\u4ed6\u5173\u4e8e\u6570\u636e\u7684\u63cf\u8ff0\u6027\u4fe1\u606f'),
        ),
        migrations.AlterField(
            model_name='map',
            name='title_en',
            field=models.CharField(help_text='\u7528\u5df2\u77e5\u8d44\u6e90\u547d\u540d', max_length=255, null=True, verbose_name='\u6807\u9898'),
        ),
        migrations.AlterField(
            model_name='map',
            name='urlsuffix',
            field=models.CharField(max_length=255, verbose_name='\u7f51\u7ad9\u7f51\u5740', blank=True),
        ),
        migrations.AlterField(
            model_name='map',
            name='zoom',
            field=models.IntegerField(verbose_name='\u7f29\u653e'),
        ),
        migrations.AlterField(
            model_name='maplayer',
            name='fixed',
            field=models.BooleanField(default=False, verbose_name='\u56fa\u5b9a'),
        ),
        migrations.AlterField(
            model_name='maplayer',
            name='format',
            field=models.CharField(max_length=200, null=True, verbose_name='\u683c\u5f0f', blank=True),
        ),
        migrations.AlterField(
            model_name='maplayer',
            name='group',
            field=models.CharField(max_length=200, null=True, verbose_name='\u7ec4', blank=True),
        ),
        migrations.AlterField(
            model_name='maplayer',
            name='layer_params',
            field=models.TextField(verbose_name='\u56fe\u5c42\u53c2\u6570'),
        ),
        migrations.AlterField(
            model_name='maplayer',
            name='name',
            field=models.CharField(max_length=200, null=True, verbose_name='\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='maplayer',
            name='opacity',
            field=models.FloatField(default=1.0, verbose_name='\u900f\u660e\u5ea6'),
        ),
        migrations.AlterField(
            model_name='maplayer',
            name='ows_url',
            field=models.URLField(null=True, verbose_name='OWS\u7f51\u5740', blank=True),
        ),
        migrations.AlterField(
            model_name='maplayer',
            name='source_params',
            field=models.TextField(verbose_name='\u6570\u636e\u6e90\u53c2\u6570'),
        ),
        migrations.AlterField(
            model_name='maplayer',
            name='stack_order',
            field=models.IntegerField(verbose_name='\u91cd\u53e0\u987a\u5e8f'),
        ),
        migrations.AlterField(
            model_name='maplayer',
            name='styles',
            field=models.CharField(max_length=200, null=True, verbose_name='\u6837\u5f0f', blank=True),
        ),
        migrations.AlterField(
            model_name='maplayer',
            name='transparent',
            field=models.BooleanField(default=False, verbose_name='\u900f\u660e'),
        ),
        migrations.AlterField(
            model_name='maplayer',
            name='visibility',
            field=models.BooleanField(default=True, verbose_name='\u80fd\u89c1\u5ea6'),
        ),
        migrations.AlterField(
            model_name='mapsnapshot',
            name='config',
            field=models.TextField(verbose_name='JSON\u914d\u7f6e'),
        ),
    ]
