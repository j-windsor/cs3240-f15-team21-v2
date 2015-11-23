# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_contributor'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='contributor_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=300), size=None, default=''),
        ),
    ]
