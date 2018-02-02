# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import taggit.managers
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_auto_20171114_0341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactrole',
            name='role',
            field=models.CharField(help_text='\u8d23\u4efb\u65b9\u5c65\u884c\u804c\u52a1', max_length=255, choices=[(b'author', '\u8d44\u6e90\u6388\u6743\u65b9'), (b'processor', '\u8d44\u6e90\u4fee\u6539\u65b9'), (b'publisher', '\u8d44\u6e90\u53d1\u5e03\u65b9'), (b'custodian', '\u63a5\u53d7\u95ee\u8d23\u548c\u8d23\u4efb\u7684\u6570\u636e\uff0c\u5e76\u786e\u4fdd\u8d44\u6e90\u7684\u9002\u5f53\u7684\u7ef4\u62a4\u548c\u4fdd\u517b\u65b9'), (b'pointOfContact', '\u8d44\u6e90\u4fe1\u606f\u67e5\u8be2\u65b9'), (b'distributor', '\u8d44\u6e90\u5206\u914d\u65b9'), (b'user', '\u8d44\u6e90\u4f7f\u7528\u65b9'), (b'resourceProvider', '\u8d44\u6e90\u63d0\u4f9b\u65b9'), (b'originator', '\u8d44\u6e90\u5236\u9020\u65b9'), (b'owner', '\u8d44\u6e90\u62e5\u6709\u65b9'), (b'principalInvestigator', '\u4fe1\u606f\u6536\u96c6\u4e0e\u7814\u7a76\u7684\u4e3b\u8981\u8d23\u4efb\u65b9')]),
        ),
        migrations.AlterField(
            model_name='link',
            name='extension',
            field=models.CharField(help_text='\u6bd4\u5982\u201ckml\u201d', max_length=255),
        ),
        migrations.AlterField(
            model_name='link',
            name='mime',
            field=models.CharField(help_text='\u6bd4\u5982\u201ctext/xml\u201d', max_length=255),
        ),
        migrations.AlterField(
            model_name='link',
            name='name',
            field=models.CharField(help_text='\u6bd4\u5982\u201c\u5728\u8c37\u6b4c\u5730\u7403\u4e2d\u67e5\u770b\u201d', max_length=255),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='abstract',
            field=models.TextField(help_text='\u8d44\u6599\u7b80\u4ecb', max_length=2000, verbose_name='\u6458\u8981', blank=True),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='category',
            field=models.ForeignKey(blank=True, to='base.TopicCategory', help_text='\u7528\u4ee5\u52a9\u4e8e\u5730\u7406\u4fe1\u606f\u641c\u96c6\u7684\u9ad8\u5c42\u6b21\u5730\u7406\u4fe1\u606f\u5206\u7c7b', null=True),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='constraints_other',
            field=models.TextField(help_text='\u4f7f\u7528\u8d44\u6599\u6216\u5143\u6570\u636e\u7684\u9650\u5236\u53ca\u6cd5\u5f8b\u524d\u63d0', null=True, verbose_name='\u5176\u4ed6\u9650\u5236', blank=True),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='csw_anytext',
            field=models.TextField(null=True, verbose_name='CSW\u6587\u672c', blank=True),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='csw_insert_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='CSW \u63d2\u5165\u65e5\u671f', null=True),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='csw_mdsource',
            field=models.CharField(default=b'local', max_length=256, verbose_name='CSW\u8d44\u6e90'),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='csw_schema',
            field=models.CharField(default=b'http://www.isotc211.org/2005/gmd', max_length=64, verbose_name='CSW \u56fe\u89e3'),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='csw_type',
            field=models.CharField(default=b'dataset', max_length=32, verbose_name='CSW\u7c7b\u578b', choices=[(b'series', '\u5e8f\u5217'), (b'software', '\u7535\u8111\u7a0b\u5e8f'), (b'featureType', '\u529f\u80fd\u7c7b\u578b'), (b'model', '\u5b58\u5728\u6216\u5047\u8bbe\u5bf9\u8c61\u7684\u526f\u672c'), (b'collectionHardware', '\u96c6\u5408\u786c\u4ef6'), (b'collectionSession', '\u96c6\u5408\u65f6\u6bb5'), (b'nonGeographicDataset', '\u975e\u5730\u7406\u6570\u636e'), (b'propertyType', '\u5c5e\u6027\u79cd\u7c7b'), (b'fieldSession', '\u7c7b\u65f6\u6bb5'), (b'dataset', '\u6570\u636e\u96c6'), (b'service', '\u670d\u52a1\u63a5\u53e3'), (b'attribute', '\u5c5e\u6027'), (b'attributeType', '\u529f\u80fd\u7279\u70b9'), (b'tile', '\u5730\u7406\u6570\u636e\u6bb5'), (b'feature', '\u529f\u80fd'), (b'dimensionGroup', '\u7ef4\u5ea6\u7ec4')]),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='csw_typename',
            field=models.CharField(default=b'gmd:MD_Metadata', max_length=32, verbose_name='CSW\u7c7b\u578b\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='csw_wkt_geometry',
            field=models.TextField(default=b'POLYGON((-180 -90,-180 90,180 90,180 -90,-180 -90))', verbose_name='CSW WKT\u51e0\u4f55\u56fe\u5f62'),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='data_quality_statement',
            field=models.TextField(help_text='\u5bf9\u4e8e\u6570\u636e\u96c6\u6cbf\u88ad\u7684\u57fa\u672c\u77e5\u8bc6', max_length=2000, null=True, verbose_name='\u6570\u636e\u8d28\u91cf\u63cf\u8ff0', blank=True),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now, help_text='\u8d44\u6599\u5f15\u7528\u65e5\u671f', verbose_name='\u65e5\u671f'),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='date_type',
            field=models.CharField(default=b'publication', help_text='\u7279\u5b9a\u4e8b\u4ef6\u53d1\u751f\u7684\u6807\u8bc6\u7801', max_length=255, verbose_name='\u65e5\u671f\u7c7b\u578b', choices=[(b'creation', 'Creation'), (b'publication', 'Publication'), (b'revision', 'Revision')]),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='edition',
            field=models.CharField(help_text='\u5f15\u7528\u6587\u732e\u7684\u7248\u672c', max_length=255, null=True, verbose_name='\u7248\u672c', blank=True),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='featured',
            field=models.BooleanField(default=False, help_text='\u8fd9\u4e2a\u8d44\u6e90\u5e94\u8be5\u53d1\u5e03\u5230\u4e3b\u9875\u4e0a\u5417\uff1f', verbose_name='\u7279\u5f81\u7269'),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='is_published',
            field=models.BooleanField(default=True, help_text='\u5982\u679c\u8fd9\u4e2a\u8d44\u6e90\u53d1\u5e03\u4e0e\u68c0\u7d22\uff1f', verbose_name='\u5df2\u53d1\u5e03'),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='keywords',
            field=taggit.managers.TaggableManager(to='base.HierarchicalKeyword', through='base.TaggedContentItem', blank=True, help_text='\u5e38\u7528\u8bcd\u6c47\u6216\u56fa\u5b9a\u77ed\u8bed(\u7528\u7a7a\u683c\u6216\u9017\u53f7\u9694\u5f00', verbose_name='\u5173\u952e\u5b57'),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='language',
            field=models.CharField(default=b'eng', help_text='\u6570\u636e\u96c6\u4f7f\u7528\u8bed\u8a00', max_length=3, verbose_name='\u8bed\u8a00', choices=[(b'abk', b'Abkhazian'), (b'aar', b'Afar'), (b'afr', b'Afrikaans'), (b'amh', b'Amharic'), (b'ara', b'Arabic'), (b'asm', b'Assamese'), (b'aym', b'Aymara'), (b'aze', b'Azerbaijani'), (b'bak', b'Bashkir'), (b'ben', b'Bengali'), (b'bih', b'Bihari'), (b'bis', b'Bislama'), (b'bre', b'Breton'), (b'bul', b'Bulgarian'), (b'bel', b'Byelorussian'), (b'cat', b'Catalan'), (b'cos', b'Corsican'), (b'dan', b'Danish'), (b'dzo', b'Dzongkha'), (b'eng', b'English'), (b'fra', b'French'), (b'epo', b'Esperanto'), (b'est', b'Estonian'), (b'fao', b'Faroese'), (b'fij', b'Fijian'), (b'fin', b'Finnish'), (b'fry', b'Frisian'), (b'glg', b'Gallegan'), (b'ger', b'German'), (b'gre', b'Greek'), (b'kal', b'Greenlandic'), (b'grn', b'Guarani'), (b'guj', b'Gujarati'), (b'hau', b'Hausa'), (b'heb', b'Hebrew'), (b'hin', b'Hindi'), (b'hun', b'Hungarian'), (b'ind', b'Indonesian'), (b'ina', b'Interlingua (International Auxiliary language Association)'), (b'iku', b'Inuktitut'), (b'ipk', b'Inupiak'), (b'ita', b'Italian'), (b'jpn', b'Japanese'), (b'kan', b'Kannada'), (b'kas', b'Kashmiri'), (b'kaz', b'Kazakh'), (b'khm', b'Khmer'), (b'kin', b'Kinyarwanda'), (b'kir', b'Kirghiz'), (b'kor', b'Korean'), (b'kur', b'Kurdish'), (b'oci', b"Langue d 'Oc (post 1500)"), (b'lao', b'Lao'), (b'lat', b'Latin'), (b'lav', b'Latvian'), (b'lin', b'Lingala'), (b'lit', b'Lithuanian'), (b'mlg', b'Malagasy'), (b'mlt', b'Maltese'), (b'mar', b'Marathi'), (b'mol', b'Moldavian'), (b'mon', b'Mongolian'), (b'nau', b'Nauru'), (b'nep', b'Nepali'), (b'nor', b'Norwegian'), (b'ori', b'Oriya'), (b'orm', b'Oromo'), (b'pan', b'Panjabi'), (b'pol', b'Polish'), (b'por', b'Portuguese'), (b'pus', b'Pushto'), (b'que', b'Quechua'), (b'roh', b'Rhaeto-Romance'), (b'run', b'Rundi'), (b'rus', b'Russian'), (b'smo', b'Samoan'), (b'sag', b'Sango'), (b'san', b'Sanskrit'), (b'scr', b'Serbo-Croatian'), (b'sna', b'Shona'), (b'snd', b'Sindhi'), (b'sin', b'Singhalese'), (b'ssw', b'Siswant'), (b'slv', b'Slovenian'), (b'som', b'Somali'), (b'sot', b'Sotho'), (b'spa', b'Spanish'), (b'sun', b'Sudanese'), (b'swa', b'Swahili'), (b'tgl', b'Tagalog'), (b'tgk', b'Tajik'), (b'tam', b'Tamil'), (b'tat', b'Tatar'), (b'tel', b'Telugu'), (b'tha', b'Thai'), (b'tir', b'Tigrinya'), (b'tog', b'Tonga (Nyasa)'), (b'tso', b'Tsonga'), (b'tsn', b'Tswana'), (b'tur', b'Turkish'), (b'tuk', b'Turkmen'), (b'twi', b'Twi'), (b'uig', b'Uighur'), (b'ukr', b'Ukrainian'), (b'urd', b'Urdu'), (b'uzb', b'Uzbek'), (b'vie', b'Vietnamese'), (b'vol', b'Volap\xc3\xbck'), (b'wol', b'Wolof'), (b'xho', b'Xhosa'), (b'yid', b'Yiddish'), (b'yor', b'Yoruba'), (b'zha', b'Zhuang'), (b'zul', b'Zulu')]),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='license',
            field=models.ForeignKey(blank=True, to='base.License', help_text='\u6570\u636e\u96c6\u7684\u8bb8\u53ef', null=True, verbose_name='\u8bb8\u53ef'),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='maintenance_frequency',
            field=models.CharField(choices=[(b'unknown', '\u7ef4\u62a4\u6570\u636e\u7684\u9891\u7387\u672a\u77e5'), (b'continual', '\u6570\u636e\u88ab\u53cd\u590d\u9891\u7e41\u5730\u66f4\u65b0'), (b'notPlanned', '\u6ca1\u6709\u66f4\u65b0\u6570\u636e\u7684\u8ba1\u5212'), (b'daily', '\u6570\u636e\u6bcf\u5929\u66f4\u65b0\u4e00\u6b21'), (b'annually', '\u6570\u636e\u6bcf\u5e74\u66f4\u65b0\u4e00\u6b21'), (b'asNeeded', '\u6570\u636e\u4e00\u7ecf\u9700\u8981\u5e76\u66f4\u65b0\u4e00\u6b21'), (b'monthly', '\u6570\u636e\u6bcf\u6708\u66f4\u65b0\u4e00\u6b21'), (b'fortnightly', '\u6570\u636e\u6bcf\u4e24\u5468\u66f4\u65b0\u4e00\u6b21'), (b'irregular', '\u4e0a\u4f20\u6570\u636e\u7684\u65f6\u95f4\u95f4\u9694\u4e0d\u4e00\u81f4'), (b'weekly', '\u6570\u636e\u6bcf\u5468\u66f4\u65b0\u4e00\u6b21'), (b'biannually', '\u6570\u636e\u4e00\u5e74\u66f4\u65b0\u4e24\u6b21'), (b'quarterly', '\u6570\u636e\u6bcf\u4e09\u4e2a\u6708\u66f4\u65b0\u4e00\u6b21')], max_length=255, blank=True, help_text='\u6570\u636e\u9996\u6b21\u751f\u6210\u540e\u7684\u4fee\u6539\u53ca\u5220\u9664\u9891\u7387', null=True, verbose_name='\u7ef4\u62a4\u9891\u7387'),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='owner',
            field=models.ForeignKey(related_name='owned_resource', verbose_name='\u6240\u6709\u8005', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='purpose',
            field=models.TextField(help_text='\u603b\u7ed3\u751f\u6210\u8d44\u6e90\u7684\u52a8\u673a', max_length=500, null=True, verbose_name='\u76ee\u6807', blank=True),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='regions',
            field=models.ManyToManyField(help_text='\u5b9a\u4f4d\u5173\u952e\u8bcd', to='base.Region', verbose_name='\u5173\u952e\u8bcd\u533a\u57df', blank=True),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='restriction_code_type',
            field=models.ForeignKey(blank=True, to='base.RestrictionCodeType', help_text='\u9650\u5236\uff08\u591a\u4e2a\uff09\u653e\u7f6e\u5728\u6240\u8ff0\u6570\u636e\u7684\u8bbf\u95ee\u6216\u4f7f\u7528\u3002', null=True, verbose_name='\u9650\u5236'),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='spatial_representation_type',
            field=models.ForeignKey(blank=True, to='base.SpatialRepresentationType', help_text='\u65b9\u6cd5\u7528\u4e8e\u8868\u793a\u6570\u636e\u96c6\u4e2d\u7684\u5730\u7406\u4fe1\u606f\u3002', null=True, verbose_name='\u7a7a\u95f4\u5448\u73b0\u7c7b\u578b'),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='supplemental_information',
            field=models.TextField(default='\u65e0\u4fe1\u606f\u63d0\u4f9b', help_text='\u5176\u4ed6\u5173\u4e8e\u6570\u636e\u7684\u63cf\u8ff0\u6027\u4fe1\u606f', max_length=2000, verbose_name='\u8865\u5145\u4fe1\u606f'),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='temporal_extent_end',
            field=models.DateTimeField(help_text='\u6570\u636e\u96c6\u6240\u8986\u76d6\u65f6\u95f4\u6bb5 (\u7ed3\u675f\u65e5\u671f)', null=True, verbose_name='\u7ed3\u675f\u65f6\u95f4', blank=True),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='temporal_extent_start',
            field=models.DateTimeField(help_text='\u6570\u636e\u96c6\u6240\u8986\u76d6\u65f6\u95f4\u6bb5 (\u8d77\u59cb\u65e5\u671f)', null=True, verbose_name='\u8d77\u59cb\u65f6\u95f4', blank=True),
        ),
        migrations.AlterField(
            model_name='resourcebase',
            name='title',
            field=models.CharField(help_text='\u7528\u5df2\u77e5\u8d44\u6e90\u547d\u540d', max_length=255, verbose_name='\u6807\u9898'),
        ),
    ]
