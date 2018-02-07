# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0027_auto_20171231_1912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='map',
            old_name='abstract_en',
            new_name='abstract_zh_cn',
        ),
        migrations.RenameField(
            model_name='map',
            old_name='constraints_other_en',
            new_name='constraints_other_zh_cn',
        ),
        migrations.RenameField(
            model_name='map',
            old_name='data_quality_statement_en',
            new_name='data_quality_statement_zh_cn',
        ),
        migrations.RenameField(
            model_name='map',
            old_name='purpose_en',
            new_name='purpose_zh_cn',
        ),
        migrations.RenameField(
            model_name='map',
            old_name='supplemental_information_en',
            new_name='supplemental_information_zh_cn',
        ),
        migrations.RenameField(
            model_name='map',
            old_name='title_en',
            new_name='title_zh_cn',
        ),
        migrations.AlterField(
            model_name='map',
            name='content_map',
            field=models.TextField(default='<h3>\u5173\u4e8e\u6211\u4eec</h3>  <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  \u707f\u70c2\u8f89\u714c\u7684\u4eba\u7c7b\u6587\u660e\u3001\u6d69\u5982\u70df\u6d77\u7684\u53e4\u4eca\u6587\u732e\u4ee5\u53ca\u5e7f\u88a4\u65e0\u57a0\u7684  \u9646\u5730\u6d77\u6d0b\uff0c\u5b58\u5728\u7740\u6d77\u91cf\u7684\u4e0e\u4eba\u7c7b\u6d3b\u52a8\u606f\u606f\u76f8\u5173\u7684\u5730\u7406\u4fe1\u606f\u3002  \u5c31\u5355\u4e2a\u4eba\u7269\u6765\u8bf4\uff0c\u5305\u62ec\u4eba\u7269\u7684\u7c4d\u8d2f\u3001\u884c\u8ff9\u3001\u793e\u4f1a\u5173\u7cfb\u7684\u5730\u7406\u5206\u5e03\uff1b  \u5c31\u7fa4\u4f53\u6765\u8bf4\uff0c\u5305\u62ec\u4e00\u4e2a\u7fa4\u4f53\u7684\u5730\u7406\u5206\u5e03\u548c\u8fc1\u5f99\u8f68\u8ff9\uff1b\u5c31\u975e\u751f\u547d  \u7684\u7269\u4f53\u6765\u8bf4\uff0c\u4e5f\u6709\u5176\u5b58\u5728\u3001\u5206\u5e03\u548c\u53d8\u5316\u7684\u5730\u7406\u533a\u57df\uff1b\u5c31\u4e00\u4e2a\u5730  \u65b9\u6765\u8bf4\uff0c\u5219\u53c8\u5305\u542b\u4e86\u65e2\u5f80\u65f6\u95f4\u91cc\u4eba\u3001\u4e8b\u3001\u7269\u7b49\u5730\u7406\u4fe1\u606f\u7684\u603b\u6c47\u3002</p>  <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  \u7531\u6d59\u6c5f\u5927\u5b66\u4e0e\u54c8\u4f5b\u5927\u5b66\u5171\u5efa\u7684\u5b66\u672f\u5730\u56fe\u53d1\u5e03\u5e73\u53f0\u613f\u4e3a\u5e7f\u5927  \u7528\u6237\u63d0\u4f9b\u5730\u7406\u4fe1\u606f\u7814\u7a76\u6210\u679c\u7684\u53d1\u5e03\u3001\u53ef\u89c6\u5316\u5206\u6790\u53ca\u591a\u529f\u80fd\u67e5  \u8be2\u670d\u52a1\uff0c\u5e73\u53f0\u6240\u5f62\u6210\u7684\u5927\u6570\u636e\uff0c\u53ef\u4ee5\u4e3a\u672a\u6765\u79d1\u5b66\u7814\u7a76\u3001\u653f\u5e9c\u51b3  \u7b56\u53ca\u793e\u4f1a\u670d\u52a1\u63d0\u4f9b\u91cd\u8981\u7684\u53c2\u8003\u3002</p>  <p style="text-align: right">\u6d59\u6c5f\u5927\u5b66\u5927\u6570\u636e\u4e0e\u4e2d\u56fd\u5b66\u672f\u5730\u56fe\u521b\u65b0\u56e2\u961f<br>  \u54c8\u4f5b\u5927\u5b66\u5730\u7406\u5206\u6790\u4e2d\u5fc3<br>  2017\u5e7412\u670818\u65e5<br></p>  <h3>\u7248\u6743\u58f0\u660e</h3>  <p>\u3000&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  \u201c\u5b66\u672f\u5730\u56fe\u53d1\u5e03\u5e73\u53f0\u201d\u7684\u7248\u6743\u5f52\u201c\u6d59\u6c5f\u5927\u5b66\u5927\u6570\u636e\u4e0e\u4e2d\u56fd\u5b66\u672f  \u5730\u56fe\u521b\u65b0\u56e2\u961f\u201d\u548c\u201c\u54c8\u4f5b\u5927\u5b66\u5730\u7406\u5206\u6790\u4e2d\u5fc3\u201d\u5171\u540c\u6240\u6709\u3002\u5b66\u8005\u4e0a\u4f20\u7684  \u5730\u7406\u4fe1\u606f\u6570\u636e\u4e0e\u5448\u73b0\u7684\u5730\u56fe\uff0c\u7248\u6743\u5f52\u53d1\u5e03\u8005\u548c\u5e73\u53f0\u65b9\u5171\u540c\u6240\u6709\u3002</p>', null=True, verbose_name='Site Content', blank=True),
        ),
    ]
