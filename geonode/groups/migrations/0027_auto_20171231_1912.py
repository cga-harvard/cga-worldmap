# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '26_to_27'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupinvitation',
            name='role',
            field=models.CharField(max_length=10, choices=[(b'manager', '\u7ecf\u7406'), (b'member', '\u4f1a\u5458')]),
        ),
        migrations.AlterField(
            model_name='groupinvitation',
            name='state',
            field=models.CharField(default=b'sent', max_length=10, choices=[(b'sent', '\u53d1\u9001'), (b'accepted', '\u63a5\u53d7'), (b'declined', '\u62d2\u7edd')]),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='role',
            field=models.CharField(max_length=10, choices=[(b'manager', '\u7ecf\u7406'), (b'member', '\u4f1a\u5458')]),
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='access',
            field=models.CharField(default=b"public'", help_text='\u5e02\u6c11\uff1a\u4efb\u4f55\u6ce8\u518c\u7528\u6237\u90fd\u53ef\u4ee5\u67e5\u770b\u5e76\u52a0\u5165\u5927\u4f17\u96c6\u56e2\u3002 <br>\u516c\u5f00\uff08\u9080\u8bf7\u53ea\uff09\uff1a\u4efb\u4f55\u6ce8\u518c\u7528\u6237\u53ef\u4ee5\u67e5\u770b\u8be5\u7ec4\u3002\u53ea\u6709\u88ab\u9080\u8bf7\u7684\u7528\u6237\u53ef\u4ee5\u52a0\u5165\u3002 <br>\u4e2a\u4eba\uff1a\u6ce8\u518c\u7528\u6237\u65e0\u6cd5\u67e5\u770b\u6709\u5173\u7ec4\uff0c\u6210\u5458\u5305\u62ec\u4efb\u4f55\u7ec6\u8282\u3002\u53ea\u6709\u88ab\u9080\u8bf7\u7684\u7528\u6237\u53ef\u4ee5\u52a0\u5165\u3002', max_length=15, verbose_name='\u4f7f\u7528\u6743', choices=[(b'public', '\u516c\u4f17'), (b'public-invite', '\u516c\u5f00\uff08\u9080\u8bf7\u53ea\uff09'), (b'private', '\u79c1\u4eba')]),
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='description',
            field=models.TextField(verbose_name='\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='description_en',
            field=models.TextField(null=True, verbose_name='\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='email',
            field=models.EmailField(help_text='\u7535\u5b50\u90ae\u4ef6\u7528\u4e8e\u8054\u7cfb\u4e00\u4e2a\u6216\u6240\u6709\u7ec4\u6210\u5458\uff0c\u5982\u90ae\u4ef6\u5217\u8868\uff0c\u5171\u4eab\u7535\u5b50\u90ae\u4ef6\u6216\u4ea4\u6d41\u7fa4\u3002', max_length=254, null=True, verbose_name='Email', blank=True),
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='keywords',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='\u7a7a\u683c\u6216\u8005\u7528\u9017\u53f7\u9694\u5f00\u7684\u5173\u952e\u8bcd', verbose_name='\u5173\u952e\u8bcd'),
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='logo',
            field=models.ImageField(upload_to=b'people_group', verbose_name='\u6807\u5fd7', blank=True),
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='title',
            field=models.CharField(max_length=50, verbose_name='\u6807\u9898'),
        ),
        migrations.AlterField(
            model_name='groupprofile',
            name='title_en',
            field=models.CharField(max_length=50, null=True, verbose_name='\u6807\u9898'),
        ),
    ]
