#coding:utf-8
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from .models import Info
from .own_get_info import get_page_loop
from .forms import SearchForm

from bs4 import BeautifulSoup
from urllib.parse import urlencode  # 编码 URL 字符串
import time
import requests
import re
import sys

from django.forms.models import model_to_dict
import json

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger




# Create your views here.


def index(request): 
    str = request.GET.get('search')
    page_num = request.GET.get('page')
    ans = get_page_loop(15)
    for an in ans:
        if an != None:
            # insert objects unrepeatly
            Info.objects.get_or_create(title=an['title'],time=an['time'],content=an['content'])
    print("page_num",page_num)
    print("str",str)
    if str!=None or (str==None and page_num!=None) :#go to the page by page_num
        
        info_list = list(Info.objects.filter(title__contains=str))
        print("info_list_len",len(info_list))
        paginator = Paginator(info_list,5,2)# every page have 5 infos, if less than 2 then converge to the previous page
        page_num = request.GET.get('page',default='1')
        
        try:
            page = paginator.page(page_num)
            print("coming try~")
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return render(request,'infopages.html',{'info_list':page,'str':str})

    else:#go to the home page at the beginning
        form = SearchForm()
        ret_dict = {}
        print('----------bad--------------')
        ret_dict['no_post_can\'t get in'] = 'pu_gai'
        return render(request,"index.html",{'form':form})


@csrf_exempt
def infopages(request):
    str = request.GET.get('search')
    if str != None:
        print("str",str)
        #info_list = list(Info.objects.filter(title__contains=str))
        paginator = Paginator(info_list,5,2)# every page have 5 infos, if less than 2 then converge to the previous page
        page_num = request.GET.get('page',default='1')
        print("page_num",page_num)
        try:
            page = paginator.page(page_num)
            print("coming try~")
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return render(request,'infopages.html',{'info_list':page})
    else:
        print("coming here~")
        return render(request,'index.html')

def show_one_article(request):
    article_title = request.GET.get('article_title')
    article_info = list(Info.objects.filter(title=article_title))
    print(article_info)
    if article_info != None:
        return render(request,'article.html',{'article':article_info[0]})
    else:
        article_info = Info()
        article_info.title = "Sry,no such article!"
        article_info.time = ""
        article_info.content = ""
        return render(request,'article.html',{'article':article_info})

#######################################
#below are unused views, only for test#
#######################################
@csrf_exempt
def search(request):
    ans = get_page_loop(15)
    for an in ans:
        # insert objects unrepeatly
        Info.objects.get_or_create(title=an['title'],time=an['time'],content=an['content'])
        #info.title = an['title']
        #info.time = an['time']
        #info.content = an['content']
        #info.save()
    str = request.POST.get('search')
    if str!='': 
                   
        infos = Info.objects.filter(title__contains=str)
        ret_list = []
        for info in infos:
            info_dict = model_to_dict(info,fields=['title','time','content']) # convert model to dict,you can assign the attribute you want~!
            ret_list.append(info_dict)
        ret_dict = {}
        ret_dict['all'] = ret_list
        print('----------ok--------------')
        return HttpResponse(json.dumps(ret_dict),content_type='application/json')
    else:
        form = SearchForm()
        ret_dict = {}
        print('----------bad--------------')
        ret_dict['no_post_can\'t get in'] = 'pu_gai'
    return HttpResponse(json.dumps(ret_dict),content_type='application/json')


def ajax_dict(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return HttpResponse(json.dumps(name_dict), content_type='application/json')


    
    










