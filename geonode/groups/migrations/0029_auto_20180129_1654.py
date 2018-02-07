# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0028_auto_20180121_1356'),
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
        migrations.AlterField(
            model_name='groupprofile',
            name='access',
            field=models.CharField(default=b"public'", help_text='\u5e02\u6c11\uff1a\u4efb\u4f55\u6ce8\u518c\u7528\u6237\u90fd\u53ef\u4ee5\u67e5\u770b\u5e76\u52a0\u5165\u5927\u4f17\u96c6\u56e2\u3002 <br>\u516c\u5f00\uff08\u9080\u8bf7\u53ea\uff09\uff1a\u4efb\u4f55\u6ce8\u518c\u7528\u6237\u53ef\u4ee5\u67e5\u770b\u8be5\u7ec4\u3002\u53ea\u6709\u88ab\u9080\u8bf7\u7684\u7528\u6237\u53ef\u4ee5\u52a0\u5165\u3002 <br>\u4e2a\u4eba\uff1a\u6ce8\u518c\u7528\u6237\u65e0\u6cd5\u67e5\u770b\u6709\u5173\u7ec4\uff0c\u6210\u5458\u5305\u62ec\u4efb\u4f55\u7ec6\u8282\u3002\u53ea\u6709\u88ab\u9080\u8bf7\u7684\u7528\u6237\u53ef\u4ee5\u52a0\u5165\u3002', max_length=15, verbose_name='\u901a\u9053', choices=[(b'public', '\u516c\u4f17'), (b'public-invite', '\u516c\u5f00\uff08\u9080\u8bf7\u53ea\uff09'), (b'private', '\u79c1\u4eba')]),
        ),
    ]
