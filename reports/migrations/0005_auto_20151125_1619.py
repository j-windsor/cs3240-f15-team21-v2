# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_contributor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='upload_date',
            field=models.DateTimeField(verbose_name='date uploaded', auto_now_add=True),
        ),
    ]
