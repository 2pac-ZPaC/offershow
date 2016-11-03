# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0002_offerinfo_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferEvaluate',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name=b'\xe8\xaf\x84\xe4\xbb\xb7\xe7\xbc\x96\xe5\x8f\xb7', primary_key=True)),
                ('ip', models.CharField(max_length=45, null=True, verbose_name=b'\xe7\x88\x86\xe6\x96\x99\xe8\x80\x85IP', blank=True)),
                ('typeid', models.IntegerField(null=True, verbose_name=b'\xe8\xaf\x84\xe4\xbb\xb7\xe7\xb1\xbb\xe5\x9e\x8b', blank=True)),
                ('offerid', models.IntegerField(null=True, verbose_name=b'offer\xe7\xbc\x96\xe5\x8f\xb7', blank=True)),
                ('time', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'\xe8\xaf\x84\xe4\xbb\xb7\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'db_table': 'offerevaluate',
                'verbose_name': '\u85aa\u6c34\u8bc4\u4ef7',
                'verbose_name_plural': '\u85aa\u6c34\u8bc4\u4ef7',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='offerinfo',
            name='number',
            field=models.IntegerField(default=0, null=True, verbose_name=b'\xe6\xb5\x8f\xe8\xa7\x88\xe9\x87\x8f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offerinfo',
            name='score',
            field=models.IntegerField(default=3, null=True, verbose_name=b'\xe5\x8f\xaf\xe4\xbf\xa1\xe5\xba\xa6\xe8\xaf\x84\xe5\x88\x86', blank=True),
            preserve_default=True,
        ),
    ]
