#-*- coding: utf-8 -*-
#!/usr/local/bin/python

from django.shortcuts import render_to_response

def index(request):
    return render_to_response('web/index.html')
