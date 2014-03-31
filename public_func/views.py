#coding: utf-8
import json
from public_coding import xmldom,xmletree,json_code
import operator
import re
# 输出信息格式化 ->Json/Xml  默认 Json
def PFunc_OutputFomat(method, resultdict, tagname=None):
    """
    Build return respose message
    """
    out ='json'
    auth_result=''
    if 'out' in method:
        out = method['out']
    if out == 'json':
        #clearxmltag(resultdict)
        auth_result = json_code.json_encode(resultdict)
    else:
        xmldict = {}
        if tagname is not None:
            xmldict[tagname] = resultdict
        else:
            xmldict = resultdict
        xmlOperate = xmletree.EtreeCreateXMLFromDict()
        auth_result = xmlOperate.createXML(xmldict, 'utf-8')
    return auth_result

def init_result(Authenticate='False',Result='UNKNOWN_ERROR',Message='An unknown error'):
    """
      初始化返回值
    """
    import time
    result={}

    result['TimeStamp']    = time.strftime('%y%m%d%H%M%S',time.localtime(time.time()))
    result['Authenticate'] = Authenticate
    result['Message']      = Message
    result['Result']       = Result

    return auth_result

def escape_to_url(urlvalue):
    escapeCode_value = {'+':'%2B',' ':'%20','/':'%2F','?':'%3F','%':'%25','#':'%23','&':'%26','=':'%3D'}
    res = 0
    for k in escapeCode_value.iterkeys():
        try:
            res = operator.indexOf(urlvalue,k)
            urlvalue = urlvalue.replace(k,escapeCode_value.get)
        except:
            pass
    return urlvalue

def PFunc_methodobj(request):
    if request.method == 'GET':
        return request.GET
    elif request.method == 'POST':
        return request.POST
    else:
        return {}