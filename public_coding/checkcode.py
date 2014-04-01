#-*- coding: utf-8 -*-
#!/usr/local/bin/python

import time

def create_license(request, user_account, sign, count=0, overtime=21600):
    try:
        request.session['user_account'] = user_account
        request.session['sign'] = sign
        request.session['count'] = count
        request.session['overtime'] = time.time() + overtime
    except:
        return False

    return True

'''
  1 : 成功
  0 : 未发送重置邮件
  -1: 验证次数超过5次
  -2: 超时（默认6h）
  -3: 验证账户不匹配
  -4: 验证hash不匹配
'''
def check_license(request, user_account, sign):
    if 'count' in request.session:
        count = request.session['count']

        if count > 5:
            return -1
        request.session['count'] = count + 1
    else:
        return 0

    if 'overtime' in request.session:
        overtime = request.session['overtime']

        if overtime < time.time():
            return -2
    else:
        return 0

    if 'user_account' in request.session:
        ret = cmp(user_account, request.session['user_account'])

        if ret != 0:
            return -3
    else:
        return 0

    if 'sign' in request.session:
        ret = cmp(sign, request.session['sign'])

        if ret != 0:
            return -4
    else:
        return 0

    clear_license(request)

    return 1

def clear_license(request):
    try:
        if 'user_account' in request.session:
            del request.session['user_account']

        if 'sign' in request.session:
            del request.session['sign']

        if 'count' in request.session:
            del request.session['count']

        if 'overtime' in request.session:
            del request.session['overtime']

        return True
    except:
        pass

    return False