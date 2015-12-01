# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0004_auto_20151201_2116'),
    ]

    operations = [
        migrations.CreateModel(
            name='Security',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('pem_key', models.CharField(max_length=1000, default='key')),
                ('public_key', models.CharField(max_length=1000, default='key')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='keysecurity',
            name='user',
        ),
        migrations.DeleteModel(
            name='KeySecurity',
        ),
    ]
