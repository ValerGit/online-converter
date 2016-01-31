"""converter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from convert import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^converting/$', 'convert.views.proceed_convert', name='converting'),
    url(r'^$', views.home, name='view-home'),
    url(r'^signin/$', views.signin, name='view-sign-in'),
    url(r'^signup/$', views.signup, name='view-sign-up'),
    url(r'^account/$', views.account, name='view-account'),
    url(r'^graphs/$', views.graphs, name='view-graphs'),
    url(r'^ports/$', views.ports, name='view-choose-ports'),
    url(r'^tables-choose/$', views.tables, name='view-choose-tables'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='view-logout'),
    url(r'^connect/$', views.create_db),
    url(r'^get-tables/$', views.get_tables_by_db, name='get-tables'),
    url(r'^get-pulse-data/$', views.get_pulse),
]
