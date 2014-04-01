#-*- coding: utf-8 -*-
#!/usr/local/bin/python
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

class BaseMail:
    '''
    #init:
     set server address 
    '''
    def __init__(self, smtp, port, sender, pwd):
        self.smtp   = smtp
        self.port   = port
        self.sender = sender
        self.pwd    = pwd
    
    def _paraseSend(self, sSubject, sContext, sTo=''):
        if ('@163' in sTo) or ('@126' in sTo) or ('@yeah' in sTo) or ('@tom' in sTo) or ('@sina' in sTo) or ('@139' in sTo) or ('@21cn' in sTo):
            sSubject = sSubject.encode('gbk')
        return sSubject, sContext
            
    def logout(self, server):
        server.quit()                
               
    def sendHtmlorTextMail(self, sSubject, sContext, lsTo, nType):
        result = False
        mmit = MIMEMultipart('alternative')
        mmit['From'] = self.sender
        mmit['To'] = ''.join(lsTo)
        codeSubject, codeContext = self._paraseSend(sSubject, sContext, lsTo)
        mmit['Subject'] = codeSubject
        if (nType ==0):
            mmit.attach( MIMEText(codeContext, 'plain', 'utf-8'))
        else:
            mmit.attach( MIMEText(codeContext, 'html', 'utf-8'))
        try:
            server = smtplib.SMTP()
    	    #set debug level depending
            #server.set_debuglevel(1)
            server.connect(self.smtp, self.port)
            server.login(self.sender, self.pwd)
            server.ehlo()
            server.sendmail(self.sender, lsTo, mmit.as_string())
            self.logout(server)   
        except:
            return False
        return True

if __name__ == '__main__':
    g_mailsmtp = 'smtp.exmail.qq.com'
    g_mailport = 25
    g_mailsender = '376740386@qq.com'
    g_mailpwd = 'hp15859281937'

    mailClass = BaseMail(g_mailsmtp, g_mailport, g_mailsender, g_mailpwd)

    mailSubject = 'test'
    mailContent = 'aaaaaaaaaaaaaa'
    _mailAddress = 'hu.peng@autonavi.com'

    ret = mailClass.sendHtmlorTextMail(mailSubject, mailContent, _mailAddress, 0)
    print ret