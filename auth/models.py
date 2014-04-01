#-*- coding: utf-8 -*-
#!/usr/local/bin/python
from django.db import models
from django.contrib.auth.models import User

class User_Extend_Manager(models.Manager):
    def regist_user(self, username, password, email, login_ip=''):
        retUser = None
        retExtend = None

        try:
        #if True:
            retUser = User.objects.create_user(username=username, email='', password=password)
            retUser.save()

            retExtend = self.create(user=retUser.id, email=email, login_ip=login_ip)
            return retExtend.user
        except:
            if retUser:
                retUser.delete()
            if retExtend:
                retExtend.delete()
        return None

    def check_username_exist(self, username):
        ret_user = User.objects.filter(username=username)
        
        if(len(ret_user) > 0):
            return True
        else:
            return False

    def check_email_exist(self, email):
        ret_user = self.filter(email=email)
        
        if(len(ret_user) > 0):
            return True
        else:
            return False

    def reset_password(self, username, newpswd):
        ret_user = User.objects.filter(username=username)
        
        if(len(ret_user) > 0):
            ret_user[0].set_password(newpswd)
            try:
                ret_user[0].save()
                return True
            except:
                pass
        return False

    def update_logininfo(self, username, login_ip=None):
        ret_user = User.objects.filter(username=username)
        
        if(len(ret_user) > 0):
            ret_Extend = self.filter(user=ret_user[0].id)
            if(len(ret_Extend) > 0):
                ret = ret_Extend[0].m_update(login_ip=login_ip)
                if ret:
                    return True
        return False

    def get_user(self, email):
        ret_user = self.filter(email=email)
        
        if len(ret_user) > 0:
            userid = ret_user[0].user
            user = User.objects.filter(id=userid)

            return True, user[0].password[6:]
        else:
            return False, ''


class DB_User_Extend(models.Model):
    user     = models.IntegerField(default=0, primary_key=True)
    email    = models.CharField(max_length=30, blank=True)
    headimg  = models.CharField(max_length=200, blank=True)
    login_ip = models.CharField(max_length=32, blank=True)

    reserver1 = models.CharField(max_length=64, blank=True)
    reserver2 = models.CharField(max_length=32, blank=True)
    reserver3 = models.IntegerField(default=0)

    objects = User_Extend_Manager()

    def m_update(self, email=None, headimg=None, login_ip=None):
        if email:
            self.email = email
        if headimg:
            self.headimg = headimg
        if login_ip:
            self.login_ip = login_ip
        try:
            self.save()
            return True
        except:
            return False

    def m_delete(self):
        try:
            self.delete()
            return True
        except:
            self.save()
            return False
