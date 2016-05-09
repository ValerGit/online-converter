from django.contrib import admin
from models import *


@admin.register(Database)
class CategoryDatabase(admin.ModelAdmin):
    list_display = ('user', 'db_name', 'type')
    list_per_page = 10
    fields = ('user', 'type', 'db_name', 'db_user', 'db_address', 'is_deleted')


@admin.register(ConvertedDatabase)
class CategoryConvertedDb(admin.ModelAdmin):
    list_display = ('date', 'user', 'database_from', 'database_to')
    list_per_page = 10


@admin.register(InfluxTokens)
class CategoryTokens(admin.ModelAdmin):
    list_display = ('database',)
    list_per_page = 10
