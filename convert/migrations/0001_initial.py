# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConvertedDatabase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('celery_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ConvertingNotice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('converting', models.ForeignKey(to='convert.ConvertedDatabase')),
            ],
        ),
        migrations.CreateModel(
            name='Database',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(default=b'MY', max_length=2, choices=[(b'PG', b'PostgreSQL'), (b'MY', b'MySQL'), (b'MO', b'MongoDB')])),
                ('db_name', models.CharField(max_length=255)),
                ('db_user', models.CharField(max_length=255)),
                ('db_address', models.CharField(max_length=255)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DatabaseTables',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('rows_quantity', models.IntegerField()),
                ('database', models.ForeignKey(to='convert.Database')),
            ],
        ),
        migrations.AddField(
            model_name='converteddatabase',
            name='database_from',
            field=models.ForeignKey(related_name='db_from', to='convert.Database'),
        ),
        migrations.AddField(
            model_name='converteddatabase',
            name='database_to',
            field=models.ForeignKey(related_name='db_to', to='convert.Database'),
        ),
        migrations.AddField(
            model_name='converteddatabase',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
