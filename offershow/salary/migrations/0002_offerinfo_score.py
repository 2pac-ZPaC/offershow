# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerinfo',
            name='score',
            field=models.IntegerField(null=True, verbose_name=b'\xe5\x8f\xaf\xe4\xbf\xa1\xe5\xba\xa6\xe8\xaf\x84\xe5\x88\x86', blank=True),
            preserve_default=True,
        ),
    ]
