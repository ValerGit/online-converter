from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'converter.settings')

from django.conf import settings

app = Celery('converter')

app.config_from_object('django.conf:settings')
app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    return {'dict': 3, 'test': 'yes'}

from celery.utils.log import get_task_logger
import MySQLdb
import MySQLdb.cursors
from pymongo import MongoClient

logger = get_task_logger(__name__)

@app.task(bind=True)
def convert_to_mongo(self, data):
    logger.info("Start converting...")
    db = MySQLdb.connect(
        host=data['from']['host'],
        user=data['from']['user'],
        passwd=data['from']['password'],
        db=data['from']['db'],
        cursorclass=MySQLdb.cursors.DictCursor
    )

    uri = 'mongodb://'
    if data['to']['user'] != '' and data['to']['password'] != '':  # !!!
        uri += data['to']['user'] + ':' + data['to']['password'] + '@'
    uri += data['to']['host'] + '/' + data['to']['db']

    client = MongoClient(uri)
    mongo_db = client[data['to']['db']]

    cur = db.cursor()
    # cur.execute("show tables")
    # for row in cur.fetchall():
    #     logger.info(row[0])

    for t in data['tables']:
        if not t['isEmbedded']:
            convert(data['tables'], t, cur, mongo_db)


def convert(tables, current_table, cursor, mongo_db):
    cursor.execute('SELECT * FROM ' + current_table['name'])
    collection = mongo_db[current_table['name']]
    for row in cursor.fetchall():
        inserted_id = collection.insert_one(row).inserted_id
        print inserted_id
        break

    embed = (t for t in tables if t['isEmbedded'] and t['embeddedIn'] == current_table['name'])
    for t in embed:
        convert(tables, t, cursor, mongo_db)