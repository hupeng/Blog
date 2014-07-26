#-*- coding: utf-8 -*-
#!/usr/local/bin/python

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^3d-demo/?', 'website.views.demo', name='demo'),
)