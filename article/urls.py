#-*- coding: utf-8 -*-
#!/usr/local/bin/python

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # 发布文章
    url(r'^publish/?$', 'article.views.publish', name='publish'),
    # 
    
)