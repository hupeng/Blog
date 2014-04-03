#-*- coding: utf-8 -*-
#!/usr/local/bin/python

from auth.models import *
from django.contrib.auth import authenticate, login, logout
from public_define.pub_define import G_DOMAIN
from public_func.views import init_result
from public_coding import checkcode
from public_coding.views import send_resetpd_email

import re, time, hashlib

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
            result['is_super'] = bool(request.user.is_superuser)
    else:
        result['Authenticate'] = 'False'
        result['Result']       = 'FAIL'
        result['Error']        = 'ERROR_NOT_LOGINED'
        result['Message']      = 'you have not logined'

    return result

def check_email_registered(email):
    pattern = re.compile(r'^(\w)+(\.\w+)*@(\w)+((\.\w{2,3}){1,3})$')

    if pattern.match(email):
        
        ret = DB_User_Extend.objects.check_email_exist(email)
        if ret:
            return 1     # 邮箱已被注册
        else:
            return 2     # 邮箱未被注册

    return 0             # 邮箱不合法

#--------------------for views--------------------------------------------
def User_Regist(methodobj):
    result = init_result()

    if("user_account" in methodobj) and ("user_password" in methodobj):
        user_account  = methodobj.get("user_account")
        user_password = methodobj.get("user_password")

        ret_check = check_email_registered(user_account)

        if ret_check == 2:  
            ret_regist = DB_User_Extend.objects.regist_user(username=user_account, password=user_password, email=user_account)
            
            if ret_regist:
                result['Result']  = 'SUCCESS'
                result['Message'] = 'regist success'
            else:
                result['Result']  = 'FAIL' 
                result['Error']   = 'ERROR_USER_CREATE'
                result['Message'] = 'create user fail'
        elif ret_check == 1:
            result['Result']  = 'FAIL' 
            result['Error']   = 'ERROR_EMAIL_REGISTED'
            result['Message'] = 'email have been registed'
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
                del result['Error']
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
    result = User_CheckLogin(methodobj, request)

    if result['Result'] == 'SUCCESS':
        del result['userid']
        del result['username']

        if('old_password' in methodobj) and ('user_password' in methodobj) and ('repeat_pd' in methodobj):
            oldpd     = methodobj.get('old_password')
            userpd    = methodobj.get('user_password')
            repeat_pd = methodobj.get('repeat_pd')

            if cmp(userpd, repeat_pd) == 0:
                try:
                #if True:
                    if request.user.check_password(oldpd):
                        request.user.set_password(userpd)
                        request.user.save()

                        logout(request)

                        result['Result'] = 'SUCCESS'
                        result['Message'] = 'update password success'
                    else:
                        result['Result'] = 'FAIL'
                        result['Message'] = 'The old password wrong'
                        result['Error']  = 'ERROR_OLD_PASSWORD'
                except:
                    result['Result'] = 'FAIL'
                    result['Message'] = 'Service error'
                    result['Error'] = 'ERROR_SERVICE'
            else:
                result['Result']  = 'FAIL'
                result['Message'] = 'new_password and repeat_password do not match'
                result['Error']   = 'ERROR_NOT_MATCH'
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

def User_Send_Email(methodobj, request):
    result = init_result()

    if 'user_account' in methodobj:
        user_account = methodobj.get('user_account')

        ret, pd_hash = DB_User_Extend.objects.get_user(user_account)
        if ret:
            source = user_account + pd_hash + str(time.time())
            sign = hashlib.md5(source).hexdigest()

            checkcode.create_license(request, user_account, sign)

            checkuri = G_DOMAIN + '/auth/confirm_resetpassword/?id=' + sign
            ret_mail = send_resetpd_email(user_account, checkuri)

            if ret_mail:
                result['Result'] = 'SUCCESS'
                result['Message'] = 'send reset password email success'
            else:
                result['Result'] = 'FAIL'
                result['Message'] = 'send reset password email failed'
                result['Error'] = 'ERROR_SEND_FAIL'
        else:
            result['Result'] = 'FAIL'
            result['Message'] = 'this user_account not exist'
            result['Error'] = 'ERROR_NOT_EXIST'
    else:
        result['Result']  = 'FAIL'
        result['Message'] = 'params miss'
        result['Error']   = 'ERROR_PARAMS_MISS'

    return result


