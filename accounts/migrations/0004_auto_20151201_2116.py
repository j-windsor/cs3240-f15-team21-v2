# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_auto_20151201_2115'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeySecurity',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('pem_key', models.CharField(max_length=1000, default='key')),
                ('public_key', models.CharField(max_length=1000, default='key')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='security',
            name='user',
        ),
        migrations.DeleteModel(
            name='Security',
        ),
    ]
