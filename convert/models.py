# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Database(models.Model):
    user = models.ForeignKey(User)
    date_added = models.DateTimeField(auto_now_add=True)

    POSTGRES = 'PG'
    MYSQL = 'MY'
    MONGODB = 'MO'

    TYPE_DB_CHOICES = (
        (POSTGRES, 'PostgreSQL'),
        (MYSQL, 'MySQL'),
        (MONGODB, 'MongoDB')
    )

    type = models.CharField(max_length=2,
                            choices=TYPE_DB_CHOICES,
                            default=MYSQL)
    db_name = models.CharField(max_length=255)
    db_user = models.CharField(max_length=255)
    db_address = models.CharField(max_length=255)
    db_password = models.CharField(max_length=255, default='')
    is_deleted = models.IntegerField(default=0)

    def __unicode__(self):
        return "db name: '" + self.db_name + "' type: " + self.type

    class Meta:
        verbose_name = 'База данных'
        verbose_name_plural = 'Базы данных'


class ConvertedDatabase(models.Model):
    database_from = models.ForeignKey('Database', related_name='db_from')
    database_to = models.ForeignKey('Database', related_name='db_to')
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    celery_id = models.CharField(max_length=50)

    def __unicode__(self):
        return "'User " + self.user.username + "' converted " + self.database_from.db_name

    class Meta:
        verbose_name = 'Трансформированная база данных'
        verbose_name_plural = 'Трансформированные базы данных'


class ConvertingNotice(models.Model):
    message = models.TextField()
    converting = models.ForeignKey('ConvertedDatabase')


class DatabaseTables(models.Model):
    name = models.CharField(max_length=255)
    database = models.ForeignKey('Database')
    rows_quantity = models.IntegerField()


class InfluxTokens(models.Model):
    database = models.ForeignKey('Database')
    token = models.CharField(max_length=255)

    def __unicode__(self):
        return "'Db: " + self.database.db_name + "' of user: " + self.database.user.username

    class Meta:
        verbose_name = 'Токен InfluxDB'
        verbose_name_plural = 'Токены InfluxDB'
