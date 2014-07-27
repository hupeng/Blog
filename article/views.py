#-*- coding: utf-8 -*-
#!/usr/local/bin/python

from django.http import HttpResponse
from django.shortcuts import render_to_response
from article import form

from public_func.views import PFunc_OutputFomat, PFunc_methodobj

def index(request):
    return render_to_response('web/article.html')

def publish(request):
    methodobj = PFunc_methodobj(request)

    result = form.Article_Publish(methodobj, request)

    Out_Result = PFunc_OutputFomat(methodobj, result, 'archive')
    return HttpResponse(Out_Result)
