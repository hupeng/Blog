#-*- coding: utf-8 -*-
#!/usr/local/bin/python

from django.http import HttpResponse
from article import form

from public_func.views import PFunc_OutputFomat, PFunc_methodobj

def publish(request):
    methodobj = PFunc_methodobj(request)

    result = form.Article_Publish(methodobj, request)

    Out_Result = PFunc_OutputFomat(methodobj, result, 'archive')
    return HttpResponse(Out_Result)
