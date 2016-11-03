# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Offerinfo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name=b'offer\xe7\xbc\x96\xe5\x8f\xb7', primary_key=True)),
                ('company', models.CharField(max_length=45, null=True, verbose_name=b'\xe5\x85\xac\xe5\x8f\xb8\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('position', models.CharField(max_length=45, null=True, verbose_name=b'\xe5\xb2\x97\xe4\xbd\x8d\xe5\x90\x8d\xe7\xa7\xb0', blank=True)),
                ('salary', models.CharField(max_length=45, null=True, verbose_name=b'\xe5\xb2\x97\xe4\xbd\x8d\xe8\x96\xaa\xe6\xb0\xb4', blank=True)),
                ('city', models.CharField(max_length=45, null=True, verbose_name=b'\xe5\xb7\xa5\xe4\xbd\x9c\xe5\x9c\xb0\xe7\x82\xb9', blank=True)),
                ('remark', models.CharField(max_length=45, null=True, verbose_name=b'\xe5\xb2\x97\xe4\xbd\x8d\xe5\xa4\x87\xe6\xb3\xa8', blank=True)),
                ('ip', models.CharField(max_length=45, null=True, verbose_name=b'\xe7\x88\x86\xe6\x96\x99\xe8\x80\x85IP', blank=True)),
                ('time', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'\xe7\x88\x86\xe6\x96\x99\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'db_table': 'offerinfo',
                'verbose_name': '\u85aa\u6c34\u8868\u683c',
                'verbose_name_plural': '\u85aa\u6c34\u8868\u683c',
            },
            bases=(models.Model,),
        ),
    ]
