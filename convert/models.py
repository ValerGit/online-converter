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
#    db_password = models.CharField(max_length=255)


class ConvertedDatabase(models.Model):
    database_from = models.ForeignKey('Database')
    database_to = models.ForeignKey('Database')
    date = models.DateTimeField(auto_now_add=True)

    OK = 'OK'
    IN_PROGRESS = 'IP'
    CANCELLED = 'CA'
    ERROR = 'ER'

    CONVERT_STATUS_CHOICES = (
        (OK, 'OK'),
        (IN_PROGRESS, 'В прогрессе'),
        (CANCELLED, 'Отменено'),
        (ERROR, 'Ошибка')
    )

    status = models.CharField(max_length=2,
                              choices=CONVERT_STATUS_CHOICES,
                              default=OK)
    celery_id = models.CharField(max_length=50)
    completed = models.SmallIntegerField(default=0)


class ConvertingNotice(models.Model):
    message = models.TextField()
    converting = models.ForeignKey('ConvertedDatabase')


class DatabaseTables(models.Model):
    name = models.CharField(max_length=255)
    database = models.ForeignKey('Database')
    rows_quantity = models.IntegerField()