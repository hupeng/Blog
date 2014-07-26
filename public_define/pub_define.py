#coding: utf-8

"""
this file for define params of program
"""

G_DEBUG = True         #调试阶段为True  正式部署至北京服务器为False

#  =====================================================================================================================
if G_DEBUG:        # 测试版
    End = 0
    # 主域名
    G_DOMAIN = 'http://127.0.0.1:8000'


else:               # 正式发布 
    End = 0
    # 主域名
    G_DOMAIN = ''

# 发送者账号    
G_EMAIL_SENDER_NAME = 'someone@qq.com'
# 发送者账号密码
G_EMAIL_SENDER_PW   = '**********'
# smtp服务器地址
G_EMAIL_SMTP        = 'smtp.exmail.qq.com'
# smtp服务器端口
G_EMAIL_PORT        = 25
#  =====================================================================================================================

