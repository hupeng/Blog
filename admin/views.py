#-*- coding: utf-8 -*-
#!/usr/local/bin/python

from django.shortcuts import render_to_response

def publish(request):
    context = {'publish': 'item-hover'}

    return render_to_response('web/post_article.html', context)

def my_article(request):
    context = {'myArticle': 'item-hover'}
    
    return render_to_response('web/my_article.html', context)

def draft(request):
    context = {'draft': 'item-hover'}
    
    return render_to_response('web/draft.html', context)