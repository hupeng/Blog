#-*- coding: utf-8 -*-
#!/usr/local/bin/python

from django.http import HttpResponse
from django.shortcuts import render_to_response
from auth import form

from public_func.views import PFunc_OutputFomat, PFunc_methodobj

def regist(request):
    methodobj = PFunc_methodobj(request)

    result = form.User_Regist(methodobj)

    Out_Result = PFunc_OutputFomat(methodobj, result, 'archive')
    return HttpResponse(Out_Result)

def login(request):
    methodobj = PFunc_methodobj(request)

    result = form.User_Login(methodobj, request)

    Out_Result = PFunc_OutputFomat(methodobj, result, 'archive')
    return HttpResponse(Out_Result)

def logout(request):
    methodobj = PFunc_methodobj(request)

    result = form.User_Logout(request)

    Out_Result = PFunc_OutputFomat(methodobj, result, 'archive')
    return HttpResponse(Out_Result)


def updatepassword(request):
    methodobj = PFunc_methodobj(request)

    result = form.User_Update_Password(methodobj, request)

    Out_Result = PFunc_OutputFomat(methodobj, result, 'archive')
    return HttpResponse(Out_Result)

def resetpassword(request):
    methodobj = PFunc_methodobj(request)

    result = form.User_Reset_Password(methodobj)

    Out_Result = PFunc_OutputFomat(methodobj, result, 'archive')
    return HttpResponse(Out_Result)

def sendemail(request):
    methodobj = PFunc_methodobj(request)

    result = form.User_Send_Email(methodobj, request)

    Out_Result = PFunc_OutputFomat(methodobj, result, 'archive')
    return HttpResponse(Out_Result)

def confirm_resetpassword(request):
    methodobj = PFunc_methodobj(request)

    sign = methodobj.get('id')
    is_valid = False

    if cmp(sign, request.session.get('sign')) == 0:
        is_valid = True

    return render_to_response('web/resetpassword.html', {'is_valid': is_valid})