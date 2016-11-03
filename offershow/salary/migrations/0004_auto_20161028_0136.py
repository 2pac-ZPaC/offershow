# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0003_auto_20161026_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offerinfo',
            name='remark',
            field=models.CharField(max_length=450, null=True, verbose_name=b'\xe5\xb2\x97\xe4\xbd\x8d\xe5\xa4\x87\xe6\xb3\xa8', blank=True),
            preserve_default=True,
        ),
    ]
