#-*- coding: utf-8 -*-
#!/usr/local/bin/python

from mailbase import BaseMail
from public_define.pub_define import G_EMAIL_SENDER_NAME,G_EMAIL_SENDER_PW,G_EMAIL_SMTP,G_EMAIL_PORT
from django.shortcuts import render_to_response
import time


def send_resetpd_email(_mailAddress=None, _checkuri=None):
    g_mailsmtp   = G_EMAIL_SMTP
    g_mailport   = G_EMAIL_PORT
    g_mailsender = G_EMAIL_SENDER_NAME
    g_mailpwd    = G_EMAIL_SENDER_PW
    mailSubject  = "您提交了重置密码的申请，请检查本邮件。"

    if (_mailAddress is None) or (_checkuri is None):
        return False
    
    date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    try:
    #if True:
        mailClass = BaseMail(g_mailsmtp, g_mailport,g_mailsender, g_mailpwd)
        
        render_txt = render_to_response('web/resetpd_email.html',{'checkuri':_checkuri, 'user_account': _mailAddress, 'date': date})
        del render_txt['Content-Type']
        del render_txt['charset']
        mailContent = str(render_txt)

        return mailClass.sendHtmlorTextMail(mailSubject, mailContent, _mailAddress, 1)
    except:
        return False
