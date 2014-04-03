#-*- coding: utf-8 -*-
#!/usr/local/bin/python

from article.models import *
from public_func.views import init_result
from auth.form import User_CheckLogin

def Article_Publish(methodobj, request):
    result = User_CheckLogin(methodobj, request)

    if result['Result'] == 'SUCCESS' and result['is_super'] == True:
        author = result['userid']
        del result['userid']
        del result['username']
        del result['is_super']

        title  = methodobj.get('title', '')
        path   = methodobj.get('path', '')
        labels = methodobj.get('labels', '').split(',')
        
        if(len(title) > 0) and (len(path) > 0):
            ret_article = DB_Article.objects.publish(title, path, author, status=1)

            if ret_article:
                
                if len(labels) > 0:
                    ret_labels = DB_Labels.objects.add_labels(labels)

                    if len(ret_labels) == len(labels):
                        DB_Article_Labels.objects.add_article_labels(ret_article, labels)
                
                result['Result'] = 'SUCCESS'
                result['Message'] = 'publish article success'
            else:
                result['Result'] = 'FAIL'
                result['Message'] = 'publish article failed'
                result['Error'] = 'ERROR_PUBLISH'
        else:
            result['Result'] = 'FAIL'
            result['Message'] = 'params miss'
            result['Error'] = 'ERROR_PARAMS_MISS'

    return result



