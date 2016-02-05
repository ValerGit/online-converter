# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convert', '0003_database_is_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfluxTokens',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=255)),
                ('database', models.ForeignKey(to='convert.Database')),
            ],
        ),
    ]
