#-*- coding: utf-8 -*-
#!/usr/local/bin/python

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # 发布博客
    url(r'^publish/?$', 'admin.views.publish', name='publish'),
    # 我的博客
    url(r'^my-article/?', 'admin.views.my_article', name='my_article'),
    
)