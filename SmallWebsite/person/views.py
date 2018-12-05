import datetime

from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from user.models import UserRegister
from user.views import my_login_required
from message.models import new_messages
from person.models import *

import random,time


@my_login_required
def myVIP(request):
    mobile_num = request.session['username']
    login_user = UserRegister.objects.get(account_number=mobile_num)
    # 充钱分页
    money_charges = Money_Charge_Record.objects.filter(user=login_user)
    paginator = Paginator(money_charges,3)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request,'person/myVIP.html',{'login_flag':True,'user':login_user,'contacts':contacts})


@my_login_required
def myJF(request):
    mobile_num = request.session['username']
    login_user = UserRegister.objects.get(account_number=mobile_num)
    # 积分分页
    exchanges = Exchange_Record.objects.filter(user=login_user)
    paginator = Paginator(exchanges,3)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'person/myJF.html',{'login_flag':True,'user':login_user,'contacts':contacts})


@my_login_required
def myFB(request):
    mobile_num = request.session['username']
    user = UserRegister.objects.get(account_number=mobile_num)
    messages = new_messages.objects.filter(pub_user=user)
    # 闪开，我要开始分页了
    paginator = Paginator(messages, 3)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求不是整数，返回第一页
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的预算书范围内，返回结果的最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request,'person/myFB.html',{'login_flag':True,'contacts':contacts,'user':user,'messages':messages})


@my_login_required
def notify(request):
    mobile_num = request.session['username']
    user = UserRegister.objects.get(account_number=mobile_num)
    notifies = NotifyRec.objects.filter(comment_user=user)
    return render(request,'person/notify.html',{'login_flag':True,'notifies':notifies,'user':user})


@my_login_required
def profile(request):
    mobile_num = request.session['username']
    user = UserRegister.objects.get(account_number=mobile_num)
    if request.method == 'POST':
        user.mini_name = request.POST['nickname']
        user.account_number = request.POST['mobile_num']
        user.save()
        return HttpResponse("个人资料修改成功")
    else:
        return render(request,'person/profile.html',{'login_flag':True,'user':user})


@my_login_required
def changepwd(request):
    mobile_num = request.session['username']
    user = UserRegister.objects.get(account_number=mobile_num)
    if request.method == 'POST':
        u_mobile = request.POST['u_mobile']
        return render(request,'person/resetpwd.html',{'login_flag':True,'u_mobile':u_mobile,'user':user})
    else:
        return render(request,'person/changepwd.html',{'login_flag':True,'user':user})


@my_login_required
def resetpwd(request):
    mobile_num = request.session['username']
    user = UserRegister.objects.get(account_number=mobile_num)
    if request.method == 'POST':
        u_mobile = request.POST['u_mobile']
        resetpwduser = UserRegister.objects.get(account_number=u_mobile)
        if request.POST['ur_pwd'] != request.POST['ur_cfmpwd']:
            return render(request,'resetpwd.html',{'error':'两次密码不一致'})
        else:
            resetpwduser.password = make_password(request.POST['ur_pwd'])
            resetpwduser.save()
            return HttpResponse("密码修改成功。")
    else:
        return render(request, 'person/resetpwd.html',{'login_flag':True,'user':user})


@my_login_required
def logout(request):
    del request.session['username']
    return render(request,'person/logout.html')


# 这个充值，，这里应该有支付宝或者微信的接口，然后支付的。
# 我们就在这里面计算应该花多少钱吧——不管积分
@my_login_required
def charge(request):
    mobile_num = request.session['username']
    user = UserRegister.objects.get(account_number=mobile_num)
    charge_record = Money_Charge_Record()
    charge_record.user = user
    pubed_counts = new_messages.objects.filter(pub_user=user).filter(new_pub__year=datetime.datetime.now().year).filter(
        new_pub__month=datetime.datetime.now().month).count()
    if request.method == 'GET':
        return render(request,'person/charge.html', {'login_flag':True})
    else:
        if request.POST['chg_type'] == '1':
            if user.level > 0:
                error = "请勿重复充值"
                return render(request,'person/charge.html',{'login_flag':True,'error':error})
            # 假装支付宝里面钱够。
            if True:
                time_stamp = str(int(time.time()))
                ran_strr = ""
                for i in range(6):
                    ch = chr(random.randrange(ord('0'),ord('9')+1))
                    ran_strr += ch
                charge_record.code = ran_strr+time_stamp
                charge_record.charge_money = spend_money = 2000
                user.times = 2 - pubed_counts
                if user.times < 0:
                    user.times = 0
                user.level = 1
                user.save()
                charge_record.save()
                return HttpResponse("VIP1充值成功,花了{}大洋".format(spend_money))
            else:
                error = "钱不够"
                return render(request,'person/charge.html',{'login_flag':True,'error':error})
        elif request.POST['chg_type'] == '2':
            if user.level > 1:
                error = "请勿重复充值"
                return render(request,'person/charge.html',{'login_flag':True,'error':error})
            if user.level == 1:
                remain_money = 2000
            else:
                remain_money = 0
            if True:
                time_stamp = str(int(time.time()))
                ran_strr = ""
                for i in range(6):
                    ch = chr(random.randrange(ord('0'), ord('9') + 1))
                    ran_strr += ch
                charge_record.code = ran_strr + time_stamp
                charge_record.charge_money = spend_money = 5000 - remain_money
                user.level = 2
                # 剩余发布次数等于5 - 用户本月发布的新闻数量
                user.times = 5 - pubed_counts
                if user.times < 0:
                    user.times = 0
                user.save()
                charge_record.save()
                return HttpResponse("VIP2充值成功，花了{}大洋".format(spend_money))
            else:
                error = '钱不够'
                return render(request,'person/charge.html',{'login_flag':True,'error':error})
        elif request.POST['chg_type'] == '3':
            if user.level > 2:
                error = "请勿重复充值"
                return render(request,'person/charge.html',{'login_flag':True,'error':error})
            if user.level == 1:
                remain_money = 2000
            elif user.level == 2:
                remain_money = 5000
            else:
                remain_money = 0
            if True:
                time_stamp = str(int(time.time()))
                ran_strr = ""
                for i in range(6):
                    ch = chr(random.randrange(ord('0'), ord('9') + 1))
                    ran_strr += ch
                charge_record.code = ran_strr + time_stamp
                charge_record.charge_money = spend_money = 10000 - remain_money
                user.level = 3
                # 剩余发布次数等于5 - 用户本月发布的新闻数量
                user.times = 10 - pubed_counts
                if user.times < 0:
                    user.times = 0
                user.save()
                charge_record.save()
                return HttpResponse("VIP3充值成功,花了{}大洋".format(spend_money))
            else:
                error = '钱不够'
                return render(request,'person/charge.html',{'login_flag':True,'error':error})

        return HttpResponse("选择的VIP等级是:{},用户原有的积分:{}".format(request.POST['ex_type'],user.scores))



@my_login_required
def exchange(request):
    mobile_num = request.session['username']
    user = UserRegister.objects.get(account_number=mobile_num)
    exRecord = Exchange_Record()
    exRecord.user = user
    pubed_counts = new_messages.objects.filter(pub_user=user).filter(new_pub__year=datetime.datetime.now().year).filter(
        new_pub__month=datetime.datetime.now().month).count()
    if request.method == 'POST':
        if request.POST['ex_type'] == '1':
            if user.level > 0:
                error = "请勿重复充值"
                return render(request,'person/exchange.html',{'login_flag':True,'error':error})
            if user.scores - 20000 > 0:
                user.scores -= 20000
                exRecord.detail = "积分兑换VIP1"
                exRecord.get_or_cost = -20000
                user.times = 2 - pubed_counts
                if user.times < 0:
                    user.times = 0
                user.level = 1
                user.save()
                exRecord.save()
                return HttpResponse("VIP1充值成功")
            else:
                error = "积分不足"
                return render(request,'person/exchange.html',{'login_flag':True,'error':error})
        elif request.POST['ex_type'] == '2':
            if user.level > 1:
                error = "请勿重复充值"
                return render(request,'person/exchange.html',{'login_flag':True,'error':error})
            if user.level == 1:
                remain = 20000
            else:
                remain = 0
            if user.scores+remain - 50000 > 0:
                user.scores = user.scores+remain -50000
                exRecord.get_or_cost = remain - 50000
                exRecord.detail = "积分兑换VIP2"
                user.level = 2
                # 剩余发布次数等于5 - 用户本月发布的新闻数量
                user.times = 5 - pubed_counts
                if user.times < 0:
                    user.times = 0
                user.save()
                exRecord.save()
                return HttpResponse("VIP2充值成功")
            else:
                error = '积分不足'
                return render(request,'person/exchange.html',{'login_flag':True,'error':error})
        elif request.POST['ex_type'] == '3':
            if user.level > 2:
                error = "请勿重复充值"
                return render(request,'person/exchange.html',{'login_flag':True,'error':error})
            if user.level == 1:
                remain = 20000
            elif user.level == 2:
                remain = 50000
            else:
                remain = 0
            if user.scores+remain - 50000 > 0:
                user.scores = user.scores+remain -100000
                exRecord.get_or_cost = remain - 100000
                exRecord.detail = "积分兑换VIP3"
                user.level = 3
                # 剩余发布次数等于5 - 用户本月发布的新闻数量
                user.times = 10 - pubed_counts
                if user.times < 0:
                    user.times = 0
                user.save()
                exRecord.save()
                return HttpResponse("VIP3充值成功")
            else:
                error = '积分不足'
                return render(request,'person/exchange.html',{'login_flag':True,'error':error})

        return HttpResponse("选择的VIP等级是:{},用户原有的积分:{}".format(request.POST['ex_type'],user.scores))
    else:
        return render(request,'person/exchange.html',{'login_flag':True})