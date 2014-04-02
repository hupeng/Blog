#-*- coding: utf-8 -*-
#!/usr/local/bin/python

from django.db import models

class Article_Manager(models.Manager):
    pass

class DB_Article(models.Model):
    title   = models.CharField(max_length=100)
    author  = models.CharField(max_length=30, default="Danny")
    publish = models.DateTimeField(auto_now_add=True)
    comment = models.IntegerField(default=0)
    status  = models.IntegerField(default=0)    # 0 --- 草稿  1 --- 正式发布
    
    objects = Article_Manager()


class Labels_Manager(models.Manager):
    pass

class DB_Labels(models.Model):
    name    = models.CharField(max_length=10)
    amount  = models.IntegerField(default=1)
    
    objects = Labels_Manager()


class Article_Labels_Manager(models.Manager):
    pass

class DB_Article_Labels(models.Model):
    article_id = models.CharField(max_length=20)
    label_id   = models.CharField(max_length=20)
    
    objects    = Article_Labels_Manager()
