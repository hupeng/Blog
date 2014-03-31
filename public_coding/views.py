#-*- coding: utf-8 -*-
#!/usr/local/bin/python
from smsbase import BaseSMS
from sendmail.mailbase import BaseMail
from public_define.pub_define import G_EMAIL_SENDER_NAME,G_EMAIL_SENDER_PW,G_EMAIL_SMTP,G_EMAIL_PORT
from django.shortcuts import render_to_response

def send_sms_v2(mobile,content):
    mobilelist=[]
    mobilelist.append(str(mobile))
    try:
    #if True:
        licensesms = BaseSMS()
        ret, error_msg, error_code = licensesms.sendSMS_v2(mobilelist=mobilelist,content=content)
        return ret, error_msg, error_code
    except:
        return False, 'send msg fail', 'ERROR_SENDMSG_FAIL'

def send_checkcode_email(_mailAddress=None, _checkcode=None):
    g_mailsmtp = G_EMAIL_SMTP
    g_mailport = G_EMAIL_PORT
    g_mailsender   = G_EMAIL_SENDER_NAME
    g_mailpwd = G_EMAIL_SENDER_PW
    mailSubject = "Access to Download NGI Companion App"
    if (_mailAddress is None) or (_checkcode is None):
        return False
    
    try:
    #if True:
        mailClass = BaseMail(g_mailsmtp, g_mailport,g_mailsender, g_mailpwd)
        
        render_txt = render_to_response('web/checkcode_email.txt',{'checkcode':_checkcode})
        del render_txt['Content-Type']
        del render_txt['charset']
        mailContent = str(render_txt)

        return mailClass.sendHtmlorTextMail(mailSubject, mailContent, _mailAddress, 1)
    except:
        return False
