#Requirements

* Django 1.8.4
* Celery 3.1.20
* RabbitMQ
* django-celery
* MySQLDb
* PyMongo
* django-widget-tweaks
* influxdb
* python-influxdb

### Run RabbitMQ OSX

```
cd /usr/local/sbin
sudo ./rabbitmq-server -detached
```

### Run MongoDB OSX

```
launchctl load /usr/local/Cellar/mongodb/3.0.6/homebrew.mxcl.mongodb.plist
launchctl unload /usr/local/Cellar/mongodb/3.0.6/homebrew.mxcl.mongodb.plist
```

### Run Celery

```
cd online_converter/
celery -A converter worker -l info
```
```
celery multi start worker -A converter -l info
celery multi stop worker -A converter -l info
```

### Run converter
```
gunicorn converter.wsgi -c gunicorn.conf.py --daemon
```