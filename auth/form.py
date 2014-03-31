#-*- coding: utf-8 -*-
#!/usr/local/bin/python

from auth.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, AnonymousUser
from public_func.views import init_result

import re

Encoding = 'UTF-8'

def User_CheckLogin(methodobj, request):
    result = init_result()
    
    if request.user.is_authenticated():
        username = request.user.username
        result['Message'] = 'This user already login in'
        result['Authenticate']= 'True'

        if username is not None:
            result['Result']   = 'SUCCESS'
            result['Message']  = username.encode(Encoding) + ' has already login.'
            result['username'] = username.encode(Encoding)
            result['userid']   = request.user.id
    else:
        result['Authenticate'] = 'False'
        result['Result']       = 'FAIL'
        result['Error']        = 'ERROR_NOT_LOGINED'
        result['Message']      = 'you have not logined'

    return result

def check_email_registered(email):
    pattern = re.compile(r'^(\w)+(\.\w+)*@(\w)+((\.\w{2,3}){1,3})$')

    if pattern.match(email):
        return DB_User_Extend.objects.check_email_exist(_email)

    return True

#--------------------for views--------------------------------------------
def User_Regist(methodobj):
    result = init_result()

    if("user_account" in methodobj) and ("user_password" in methodobj):
        user_account  = methodobj.get("user_account")
        user_password = methodobj.get("user_password")

        if not check_email_registered(user_account):  
            ret_regist = DB_User_Extend.objects.regist_user(username=user_account, password=user_password, email=user_account)
            
            if ret_regist:
                result['Result'] = 'SUCCESS'
            else:
                result['Result']  = 'FAIL' 
                result['Error']   = 'ERROR_USER_CREATE'
                result['Message'] = 'create user fail'
        else:
            result['Result']  = 'FAIL' 
            result['Error']   = 'ERROR_EMAIL_INVALID'
            result['Message'] = 'email invalid'

    return result

def User_Login(methodobj, request):
    result = User_CheckLogin(methodobj, request)
    
    if result['Result'] == 'FAIL':

        if('user_account' in methodobj) and ('user_password' in methodobj):
            user_account  = methodobj.get('user_account')
            user_password = methodobj.get('user_password')
            login_ip      = request.META.get('REMOTE_ADDR')

            user = authenticate(username=user_account, password=user_password)
            
            if user is not None:
                login(request, user)

                DB_User_Extend.objects.update_logininfo(username=user_account, login_ip=login_ip)

                result['Result'] = 'SUCCESS'
                result['Message'] = 'login success'
            else:
                result['Result']  = 'FAIL'
                result['Message'] = 'Authenticate failed'
                result['Error']   = 'ERROR_AUTHENTICATE'
        else:
            result['Result']  = 'FAIL'
            result['Message'] = 'params miss'
            result['Error']   = 'ERROR_PARAMS_MISS'
    
    return result

def User_Logout(request):
    result = init_result()

    logout(request)

    result['Result']  = 'SUCCESS'
    result['Message'] = 'logout success'
            
    return result

def User_Update_Password(methodobj, request):
    result = User_CheckLogin(request)

    if result['Result'] == 'SUCCESS':
        userid = result['userid']

        if('old_password' in methodobj) and ('user_password' in methodobj):
            oldpd = methodobj.get('old_password')
            userpd = methodobj.get('user_password')

            try:
            #if True:
                if request.user.check_password(oldpd):
                    request.user.set_password(userpd)
                    request.user.save()

                    logout(request)

                    result['Result'] = 'SUCCESS'
                else:
                    result['Result'] = 'FAIL'
                    result['Message'] = 'The old password wrong'
                    result['Error']  = 'ERROR_OLD_PASSWORD'
            except:
                result['Result'] = 'FAIL'
                result['Message'] = 'Service error'
                result['Error'] = 'ERROR_SERVICE'
    else:
        result['Result'] = 'FAIL'
        result['Message'] = 'you have not logined'
        result['Error'] = 'ERROR_NOT_LOGINED'
    
    return result

def User_Reset_Password(methodobj):
    result = init_result()

    if('user_account' in methodobj) and ('new_password' in methodobj) and ('repeat_pd' in methodobj):
        user_account = methodobj.get('user_account')
        new_password = methodobj.get('new_password')
        repeat_pd    = methodobj.get('repeat_pd')

        if cmp(new_password, repeat_pd) == 0:

            if len(new_password) > 5:
                ret = DB_User_Extend.objects.reset_password(user_account, new_password)

                if ret:
                    result['Result']  = 'SUCCESS'
                    result['Message'] = 'reset password success'
                else:
                    result['Result']  = 'FAIL'
                    result['Message'] = 'reset password fail'
                    result['Error']   = 'ERROR_RESET_FAIL'
            else:
                result['Result']  = 'FAIL'
                result['Message'] = 'your password too short'
                result['Error']   = 'ERROR_TOO_SHORT'
        else:
            result['Result']  = 'FAIL'
            result['Message'] = 'new_password and repeat_password do not match'
            result['Error']   = 'ERROR_NOT_MATCH'
    else:
        result['Result']  = 'FAIL'
        result['Message'] = 'params miss'
        result['Error']   = 'ERROR_PARAMS_MISS'

    return result