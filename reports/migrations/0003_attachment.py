# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import reports.models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20151101_1839'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('upload', models.FileField(upload_to=reports.models.get_upload_file_name)),
                ('key', models.CharField(max_length=100)),
                ('encrypted', models.BooleanField(default=False)),
                ('upload_date', models.DateTimeField(verbose_name='date uploaded')),
                ('report', models.ForeignKey(to='reports.Report')),
            ],
        ),
    ]
