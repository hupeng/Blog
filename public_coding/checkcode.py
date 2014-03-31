#coding: utf-8
import time, random

LICENSE_TYPE_NONE = 'none'
LICENSE_TYPE_IMG = 'img'
LICENSE_TYPE_SMS = 'sms'

RETURN_CHECK_ERROR = 0
RETURN_CHECK_SUCCESS = 1 
RETURN_IMG_CHECK_SUCCESS = 2
RETURN_SMS_CHECK_SUCCESS = 3

'''check_license 验证码验证
    返回值数组[验证结果,验证回执信息]
    验证结果 取值：0、验证失败；1、验证失败；2、图片验证码验证成功；3、短信验证码验证成功。
    回执信息 取值：LICENSE_OVERTIME：验证码过期；LICENSE_VIRES：验证码id不符；LICENSE_WRONG：验证码错误；PARAMS_ERROR：验证码错误；SMS_CHECK_SUCCESS：验证码验证成功；UNFINE_LICENSE：未生成认证码。'''
def check_license(request,checkcode,checkcodeid='',uuid=None, phone='',ischeck = False, vcode_type = 0):
    overtime=600
    
    if 'checkcode' in request.session:
        session_checkcode = request.session['checkcode']
    else:
        return RETURN_CHECK_ERROR,"UNFINE_LICENSE";
    if 'checkcode_id' in request.session:
        session_checkcode_id = request.session['checkcode_id']
    else:
        session_checkcode_id = None
    if 'checkcode_type' in request.session:
        session_checkcode_type = request.session['checkcode_type']
    else:
        session_checkcode_type = 'none'
    if 'checkcode_overtime' in request.session:
        session_checkcode_overtime = request.session['checkcode_overtime']
    else:
        session_checkcode_overtime = time.time()
    if session_checkcode_type != LICENSE_TYPE_SMS:
        clear_sms_license(request)
    if session_checkcode_overtime-time.time()<=0:
        return RETURN_CHECK_ERROR,"LICENSE_OVERTIME";
    if checkcodeid != session_checkcode_id:
        return RETURN_CHECK_ERROR,"LICENSE_VIRES"
    if checkcode != session_checkcode:
        return RETURN_CHECK_ERROR,"LICENSE_WRONG"
        
    if session_checkcode_type == LICENSE_TYPE_IMG:
        return RETURN_IMG_CHECK_SUCCESS,"OK"
    elif session_checkcode_type == LICENSE_TYPE_SMS:
        clear_sms_license(request)
        if ischeck is True:
            request.session['ischeck'] = ischeck
            request.session['phone'] = phone
            request.session['oprt_over_time'] = time.time()+overtime
            print request.session['ischeck'],request.session['phone'],request.session['oprt_over_time']
                
        return RETURN_SMS_CHECK_SUCCESS,"OK"
    else:
        return RETURN_CHECK_SUCCESS,"OK"

def create_license(request,license_id='',license_type=LICENSE_TYPE_NONE ,lon=4,overtime=600,uuid=None):
    minnum = 10**(lon-1)
    maxnum = 10**lon-1
    checkcode = str(random.randint(minnum, maxnum)) 
    request.session['checkcode'] = checkcode
    request.session['checkcode_id'] = license_id
    request.session['checkcode_type'] = license_type
    request.session['checkcode_overtime']=time.time()+overtime

    return checkcode
    
def clear_sms_license(request):
    try:
    #if True:
        if 'checkcode' in request.session:
            del  request.session['checkcode']
        if 'checkcode_id' in request.session:
            del  request.session['checkcode_id']
        if 'checkcode_type' in request.session:
            del  request.session['checkcode_type']
        if 'checkcode_overtime' in request.session:
            del  request.session['checkcode_overtime']
        return True
    except:
        return False

# return: 0:success 1:over time  2:have not check 3:phone and check phone not the same
def get_sms_check(request, phone):
    if 'ischeck' in request.session and 'phone' in request.session:
        req_ischeck = request.session['ischeck']
        req_phone = request.session['phone']

        del request.session['ischeck']
        del request.session['phone']
           
        if 'oprt_over_time' not in request.session:
            return 1
        else:
            req_oprt_over_time = request.session['oprt_over_time']
            del request.session['oprt_over_time']

            if req_oprt_over_time-time.time()<=0:
                return 1
            else:
                if req_ischeck is True:
                    if cmp(phone, req_phone) == 0:
                        return 0
                    else:
                        return 3
                else:
                    return 2
    else:
        return 2

def clear_sms_check(request):
    try:
        if 'ischeck' in request.session:
            del request.session['ischeck']
        return True
    except:
        return False

# ========================================================================================================
#
def create_thirdpart_login(request,tpid = 0, userid = 0, username='',tpuserid='',tpusername='',tptype = '', tpovertime=864000,tpuuid=None):               # tpovertime 10天
    request.session['tpid']       = tpid
    request.session['userid']     = userid
    request.session['username']   = username
    request.session['tpuserid']   = tpuserid
    request.session['tpusername'] = tpusername
    request.session['tptype']     = tptype
    request.session['tpovertime'] = time.time()+tpovertime
    request.session['tpuuid']     = tpuuid

    return tpuserid

def check_thirdpart_login(request,tpuserid='',tptype = '',uuid=None):
    result = {}
    result['Result'] = 'FAIL'
    
    if 'tpid' in request.session and 'tpuserid' in request.session and 'tpusername' in request.session and 'tptype' in request.session and 'tpovertime' in request.session and 'username' in request.session:
        req_tpid        = request.session['tpid']
        req_tpuserid    = request.session['tpuserid']
        req_tpusername  = request.session['tpusername']
        req_tptype      = request.session['tptype']
        req_tpovertime  = request.session['tpovertime']
        req_username    = request.session['username']
        req_userid      = request.session['userid']

        result['tpid']          = req_tpid
        result['tpuserid']      = req_tpuserid
        result['tpusername']    = req_tpusername
        result['tptype']        = req_tptype
        result['username']      = req_username
        result['userid']        = req_userid
        
        if cmp(tpuserid, req_tpuserid) != 0:
            clear_thirdpart_login(request)
            result['Error'] = 'ERROR_TPUSER_DIF'
            return result
        
        if cmp(tptype, req_tptype) != 0:
            clear_thirdpart_login(request)
            result['Error'] = 'ERROR_TPTYPE_DIF'
            return result
        
        if req_tpovertime - time.time() <= 0:
            clear_thirdpart_login(request)
            result['Error'] = 'ERROR_LOGIN_OVERTIME'
            return result

        result['Result'] = 'SUCCESS'
        return result
    else:
        clear_thirdpart_login(request)
        return result
    
def clear_thirdpart_login(request):
    try:
    #if True:
        if 'tpid' in request.session:
            del  request.session['tpid']
        if 'userid' in request.session:
            del  request.session['userid']
        if 'username' in request.session:
            del  request.session['username']
        if 'tpuserid' in request.session:
            del  request.session['tpuserid']
        if 'tptype' in request.session:
            del  request.session['tptype']
        if 'tpovertime' in request.session:
            del  request.session['tpovertime']
        if 'tpuuid' in request.session:
            del  request.session['tpuuid']
        return True
    except:
        return False
