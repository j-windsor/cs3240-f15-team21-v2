# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0005_report_contributor_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='contributor_list',
        ),
    ]
