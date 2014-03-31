# -*- coding: utf8 -*-
'''creater:xieyida'''
'''create time:2012-12-11'''
'''name: sent sms class'''
'''note:用于naviuser项目，按照《高德微享短信通道相关邮件内容》提供的通讯协议，开发的短信发送功能类。'''
import urllib2
import types
from xml.etree import ElementTree
from django.utils.http import urlencode
from public_define.pub_define import G_SMS_SENDER_NAME,G_SMS_SENDER_PW

SMS_BASE_URL='http://www.findpath.net:82/smmp/servletsendmoremsg.do'

class BaseSMS:
    def __init__(self,baseurl=None,name=None,password=None):
        self.baseurl = (baseurl==None or baseurl=='') and SMS_BASE_URL or  baseurl
        self.name = (name==None or name=='') and G_SMS_SENDER_NAME or  name
        self.password = (password==None or password=='') and G_SMS_SENDER_PW or  password
        if type(self.baseurl) is not types.StringType:
            raise TypeError('baseurl must be str,not '+str(type(self.baseurl)))
        if type(self.name) is not types.StringType:
            raise TypeError('name must be str,not '+str(type(self.name)))
        if type(self.password) is not types.StringType:
            raise TypeError('password must be str,not '+str(type(self.password)))

    def sendSMS(self,mobilelist,content):
        if type(mobilelist) is not types.ListType:
            raise TypeError('mobilelist must be str,not '+str(type(content)))
        if type(content) is not types.StringType:
            raise TypeError('content must be str,not '+str(type(content)))
        if len(mobilelist)<1:
            raise Exception('mobilearray can not be empty')
        if len(content)<1:
            raise Exception('content can not be empty')
        params = {}
        params['name'] = self.name
        params['password'] = self.password
        params['content'] = content.encode('gbk')
        mobilestr=''
        unique_mobiles = set(mobilelist)
        for mobileitem in unique_mobiles:
            if type(mobileitem) is not types.StringType:
                raise TypeError('mobilearray must be list<str>')
            mobilestr=mobilestr+'&mobiles='+mobileitem
        paramstr = urlencode(params)+mobilestr
        _url    = "%s?%s" % (self.baseurl, paramstr)
        _req      = urllib2.Request(url=_url, headers={ 'Accept-Language' : 'zh_CN'})
        _handler  = urllib2.urlopen( _req )
        _content = _handler.read()
        
        try:
            rootNote = ElementTree.fromstring(_content)
            reture_nodes = rootNote.getiterator("RETURN")
            reture_value = reture_nodes[0].text
            if reture_value.lower()!='true':
                error_nodes = rootNote.getiterator("ERROR")
                raise Exception(error_nodes[0].text)
        except Exception,ex:
            raise Exception(ex)
        

        return True

    def sendSMS_v2(self,mobilelist,content):
        if type(mobilelist) is not types.ListType:
            raise TypeError('mobilelist must be str,not '+str(type(content)))
        if type(content) is not types.StringType:
            raise TypeError('content must be str,not '+str(type(content)))
        if len(mobilelist)<1:
            raise Exception('mobilearray can not be empty')
        if len(content)<1:
            raise Exception('content can not be empty')
        params = {}
        params['name'] = self.name
        params['password'] = self.password
        params['content'] = content.encode('gbk')
        mobilestr=''
        unique_mobiles = set(mobilelist)
        for mobileitem in unique_mobiles:
            if type(mobileitem) is not types.StringType:
                raise TypeError('mobilearray must be list<str>')
            mobilestr=mobilestr+'&mobiles='+mobileitem
        paramstr = urlencode(params)+mobilestr
        _url    = "%s?%s" % (self.baseurl, paramstr)
        _req      = urllib2.Request(url=_url, headers={ 'Accept-Language' : 'zh_CN'})
        _handler  = urllib2.urlopen( _req )
        _content = _handler.read()
        print '_content:',_content

        rootNote = ElementTree.fromstring(_content)
        print rootNote
        reture_nodes = rootNote.getiterator("RETURN")
        print reture_nodes
        reture_value = reture_nodes[0].text
        print 'reture_value----------',reture_value
        if reture_value.lower()!='true':
            error_nodes = rootNote.getiterator("ERROR")
            print error_nodes[0].text
            ret = error_nodes[0].text.find('count>8')
            print 'ret:', ret
            if ret > 0:
                return False, error_nodes[0].text, 'ERROR_SENDMSG_MORE8'
            else:
                return False, error_nodes[0].text, 'ERROR_SENDMSG_FAIL'
        else:
            # True/False, error msg/ error code
            return True, '', ''
    
if __name__ == '__main__':
    newsms = BaseSMS()
    import datetime
    newsms.sendSMS(mobilelist=['18359206023','18359206023'],content="testMessage"+str(datetime.datetime.now()))
    print True
    

