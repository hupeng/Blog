#-*- coding: utf-8 -*-
#!/usr/local/bin/python

from django.db import models
from django.db.models import F

class Article_Manager(models.Manager):
    def publish(self, title, path, author, status=0):
        try:
            ret = self.create(title=title, path=path, author=author, status=status)
            return ret.id
        except:
            pass
        return None

class DB_Article(models.Model):
    title   = models.CharField(max_length=100)
    path    = models.CharField(max_length=150)
    author  = models.IntegerField(default=0)
    publish = models.DateTimeField(auto_now_add=True)
    comment = models.IntegerField(default=0)
    views   = models.IntegerField(default=0)
    status  = models.IntegerField(default=0)    # -1 --- 已删除 0 --- 草稿  1 --- 正式发布
    weight  = models.IntegerField(default=0)    # 值越大，排序越靠前

    reserver1 = models.CharField(max_length=64, blank=True)
    reserver2 = models.CharField(max_length=32, blank=True)
    reserver3 = models.IntegerField(default=0)
    
    objects = Article_Manager()

    def m_update(self, comment=0, views=0, status=0):
        if comment > 0:
            self.comment = F('comment') + comment
        if views > 0:
            self.views = F('views') + views
        if status > 0:
            self.status = status

        try:
            self.save()
            return True
        except:
            pass
        return False


class Labels_Manager(models.Manager):
    def add_labels(self, labels):
        ret = []

        for item in labels:
            ret_label = self.filter(name=item)
            if len(ret_label) > 0:
                ret_label[0].m_update(amount=1)
                ret.append(ret_label[0].id)
            else:
                label = self.create(name=item)
                ret.append(label.id)
        
        return ret

class DB_Labels(models.Model):
    name    = models.CharField(max_length=10)
    amount  = models.IntegerField(default=1)

    reserver1 = models.CharField(max_length=64, blank=True)
    reserver2 = models.CharField(max_length=32, blank=True)
    reserver3 = models.IntegerField(default=0)
    
    objects = Labels_Manager()

    def m_update(self, amount=0):
        if amount > 0:
            self.amount = F('amount') + amount
        try:
            self.save()
            return True
        except:
            pass
        return False


class Article_Labels_Manager(models.Manager):
    def add_article_labels(self, article_id, label_id):
        ret = self.filter(article_id=article_id)
        if len(ret) == 0:
            try:
                labels = ','.join(label_id)
                self.create(article_id=article_id, label_id=labels)
                return True
            except:
                pass
        return False

class DB_Article_Labels(models.Model):
    article_id = models.IntegerField(default=0)
    label_id   = models.CharField(max_length=200)

    reserver1 = models.CharField(max_length=64, blank=True)
    reserver2 = models.CharField(max_length=32, blank=True)
    reserver3 = models.IntegerField(default=0)
    
    objects   = Article_Labels_Manager()


class Article_Comment_Manager(models.Manager):
    pass

class DB_Article_Comment(models.Model):
    article_id = models.IntegerField(default=0)
    publisher  = models.IntegerField(default=0)
    content    = models.TextField()
    com_type   = models.IntegerField(default=0)     # 0 --- 正常   1 --- 回复
    reply      = models.CharField(max_length=200, blank=True)
    date       = models.DateTimeField(auto_now_add=True)
    status     = models.IntegerField(default=0)     # 0 --- 审核中  1 --- 通过

    reserver1 = models.CharField(max_length=64, blank=True)
    reserver2 = models.CharField(max_length=32, blank=True)
    reserver3 = models.IntegerField(default=0)

    objects   = Article_Comment_Manager()


class Article_Score_Manager(models.Manager):
    pass

class DB_Article_Score(models.Model):
    article_id = models.IntegerField(default=0)
    origin_ip  = models.CharField(max_length=32)
    score      = models.IntegerField(default=0)
    publisher  = models.IntegerField(default=0)

    reserver1 = models.CharField(max_length=64, blank=True)
    reserver2 = models.CharField(max_length=32, blank=True)
    reserver3 = models.IntegerField(default=0)

    objects   = Article_Score_Manager()

