# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convert', '0002_database_db_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='database',
            name='is_deleted',
            field=models.IntegerField(default=0),
        ),
    ]
