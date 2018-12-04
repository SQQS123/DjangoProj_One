import datetime

from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
from user.models import UserRegister
from user.views import my_login_required
from message.models import new_messages
from person.models import NotifyRecord


@my_login_required
def test(request):
    return render(request,'personalbase.html',{'login_flag':True})

@my_login_required
def myVIP(request):
    mobile_num = request.session['username']
    login_user = UserRegister.objects.get(account_number=mobile_num)
    return render(request,'person/myVIP.html',{'login_flag':True,'user':login_user})

@my_login_required
def myJF(request):
    mobile_num = request.session['username']
    login_user = UserRegister.objects.get(account_number=mobile_num)
    return render(request, 'person/myJF.html',{'login_flag':True,'user':login_user})

@my_login_required
def myFB(request):
    mobile_num = request.session['username']
    user = UserRegister.objects.get(account_number=mobile_num)
    messages = new_messages.objects.filter(pub_user=user)
    return render(request,'person/myFB.html',{'login_flag':True,'messages':messages,'user':user})

@my_login_required
def notify(request):
    mobile_num = request.session['username']
    user = UserRegister.objects.get(account_number=mobile_num)
    notifies = NotifyRecord.objects.filter(comment_user=user)
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

@my_login_required
def charge(request):
    return render(request,'person/charge.html',{'login_flag':True})

@my_login_required
def exchange(request):
    mobile_num = request.session['username']
    user = UserRegister.objects.get(account_number=mobile_num)
    if request.method == 'POST':
        if request.POST['ex_type'] == '1':
            if user.level > 0:
                error = "请勿重复充值"
                return render(request,'person/exchange.html',{'login_flag':True,'error':error})
            if user.scores - 20000 > 0:
                user.scores -= 20000
                user.times = 2 - new_messages.objects.filter(new_pub__year=datetime.datetime.now().year,
                                                             new_pub__month=datetime.datetime.now().month).count()
                if user.times < 0:
                    user.times = 0
                user.level = 1
                user.save()
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
                user.level = 2
                # 剩余发布次数等于5 - 用户本月发布的新闻数量
                user.times = 5 - new_messages.objects.filter(new_pub__year=datetime.datetime.now().year,new_pub__month=datetime.datetime.now().month).count()
                if user.times < 0:
                    user.times = 0
                user.save()
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
                user.level = 3
                # 剩余发布次数等于5 - 用户本月发布的新闻数量
                user.times = 10 - new_messages.objects.filter(new_pub__year=datetime.datetime.now().year,new_pub__month=datetime.datetime.now().month).count()
                if user.times < 0:
                    user.times = 0
                user.save()
                return HttpResponse("VIP3充值成功")
            else:
                error = '积分不足'
                return render(request,'person/exchange.html',{'login_flag':True,'error':error})

        return HttpResponse("选择的VIP等级是:{},用户原有的积分:{}".format(request.POST['ex_type'],user.scores))
    else:
        return render(request,'person/exchange.html',{'login_flag':True})