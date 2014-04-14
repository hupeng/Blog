#-*- coding: utf-8 -*-
#!/usr/local/bin/python

from django.shortcuts import render_to_response

def publish(request):
    return render_to_response('web/post_article.html')
