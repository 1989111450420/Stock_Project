from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
import matplotlib.pyplot as plt
import twstock

def login_views(request):

    if request.method == 'GET':
        if 'uphone' in request.session:
            return HttpResponseRedirect('/index/')
        else:
            if 'uphone' in request.COOKIES:
                uphone = request.COOKIES['uphone']
                request.session['uphone'] = uphone
                return HttpResponseRedirect('/index/')
            else:
                return render(request, 'login.html')

    else:
        upwd = request.POST.get('upwd', '')
        uphone = request.POST.get('uphone', '')
        if uphone and upwd:
            users = Users.objects.filter(uphone = uphone)
            if users:
                u = users[0]
                if u.upass == upwd:
                    request.session['uphone'] = u.uphone
                    if 'isSaved' in request.POST:
                        resp = HttpResponseRedirect('/index/')
                        resp.set_cookie('uphone', u.uphone, 3600 * 24 * 365)
                        return resp
                    return HttpResponseRedirect('/index/')
                else:
                    errMsg = '輸入密碼錯誤'
                    return render(request, 'login.html', locals())
            else:
                errMsg = '手機號不存在'
                return render(request, 'login.html', locals())
        else:
            errMsg = '手機號或密碼不能為空'
            return render(request, 'login.html', locals())


def register_views(request):

    if request.method == 'GET':
        return render(request, 'register.html')

    else:
        uphone = request.POST.get('uphone', '')
        upwd = request.POST.get('upwd', '')
        uname = request.POST.get('uname', '')
        uemail = request.POST.get('uemail', '')

        if uphone and upwd and uname and uemail:
            if Users.objects.filter(uphone=uphone):
                errMsg = '手機號碼已存在'
                return render(request, 'register.html', locals())
            else:
                Users.objects.create(
                    uphone=uphone, upass=upwd,
                    uname=uname, uemail=uemail,
                )
                return HttpResponse('註冊成功')
        else:
            return HttpResponse('輸入值不能為空')


def index_views(request):
    # 防止未登入就進入首頁
    if 'sessionid' in request.COOKIES:
        if request.method == 'GET':
            return render(request, 'index.html')
        else:
            search_no = request.POST.get('search_no', '')
            stock_pic(search_no)
            return render(request, 'index.html', locals())
    else:
        return HttpResponseRedirect('/login/')


def stock_pic(search_no):

    stock_real = twstock.realtime.get(search_no)
    stock_name = stock_real['info']['name']
    stock_no = twstock.Stock(search_no)
    close_price, dates = [], []
    for stock_duration in stock_no.fetch_from(2019, 6):
        close_price.append(stock_duration.close)
        dates.append(stock_duration.date)

    fig = plt.figure(dpi=80, figsize=(12, 8))
    plt.plot(dates, close_price)
    fig.autofmt_xdate(rotation=60)
    plt.title(stock_name, fontproperties="simHei", fontsize=24, )
    plt.xlabel("date", fontsize=14)
    plt.ylabel("close_price", fontsize=14)
    plt.tick_params(axis='both', labelsize=12, color='red')
    plt.show()


def logout_views(request):

    if 'sessionid' in request.COOKIES:
        resp = HttpResponseRedirect('/login/')
        resp.delete_cookie('sessionid')
        resp.delete_cookie('uphone')
        return resp
