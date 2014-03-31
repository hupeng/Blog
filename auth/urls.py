#-*- coding: utf-8 -*-
#!/usr/local/bin/python

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    #用户注册
    url(r'^regist/?$', 'auth.views.regist', name='regist'),
    #用户登录
    url(r'^login/?$', 'auth.views.login', name='login'),
    #用户退出
    url(r'^logout/?$', 'auth.views.logout', name='logout'),
    # 修改密码
    url(r'^updatepassword/?$', 'auth.views.updatepassword', name='updatepassword'),
    # 重置密码
    url(r'^resetpassword/?$', 'auth.views.resetpassword', name='resetpassword'),
)