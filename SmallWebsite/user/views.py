import datetime
import os
import random
import string
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.urls import reverse
from SmallWebsite.settings import BASE_DIR
from message.models import new_messages
from .models import UserRegister
from django.contrib.auth.hashers import make_password,check_password

import re


# django生成验证码
def get_validcode_img(request):
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # 生成一个颜色随机的大小为160,30的图片
    img = Image.new(mode="RGB", size=(160, 30), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    # 设置图片的绘制颜色
    draw = ImageDraw.Draw(img, "RGB")

    # 设置图片的绘制字体（只写字体名，会默认在系统的Fonts下去找）
    font = ImageFont.truetype(r'C:\msyh.ttf', 25)

    # 设置图片上的字符串
    valid_list = []
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_letter_low = chr(random.randint(65, 90))
        random_letter_upper = chr(random.randint(96, 122))
        random_char = random.choice([random_num, random_letter_low, random_letter_upper])  # 随机选择字符（数字，大小写字母)
        # 通过draw.text方法，设置图片上字符串的x,y坐标，字符串，颜色，字体（for循环5次，生成5个字符的验证码)
        draw.text([5+i*25, 10], random_char, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), font=font)
        valid_list.append(random_char)

    # 获取一个内存中的文件句柄
    f = BytesIO()

    # 在文件句柄中写入文件
    img.save(f, 'png')
    # 取出文件
    data = f.getvalue()
    # 转换成字符串
    valid_str = "".join(valid_list)
    print(valid_str)

    # 把验证码保存在session中，当用户出入验证码发送请求的时候，把用户输入的数据和session中的验证码做对比
    request.session["validcode"] = valid_str
    return HttpResponse(data)


# 自己的装饰器
def my_login_required(func):
    def check_login_status(request):
        if request.session.has_key('username'):
            return func(request)
        else:
            return HttpResponseRedirect('/user/login/')
    return check_login_status


# Create your views here.
def isPhone_valid(n):
    print(len(n))
    if len(n) == 11:
        if re.match(r'1[3,4,5,7,8]\d{9}', n):
            # 中国联通：
            # 130，131，132，145,155，156，185，186，145，176，175
            if re.match(r'13[0,1,2]\d{8}', n) or \
                re.match(r'145\d{8}',n) or \
                    re.match(r"15[5,6]\d{8}", n) or \
                    re.match(r"18[5,6]\d{8}", n) or \
                    re.match(r"145\d{8}", n) or \
                    re.match(r"176\d{8}", n) or \
                    re.match(r"175\d{8}",n):
                # print("该号码属于：中国联通")
                return True
            # 中国移动
            # 134, 135 , 136, 137, 138, 139, 147, 150, 151,
            # 152, 157, 158, 159, 178, 182, 183, 184, 187, 188；
            elif re.match(r"13[4,5,6,7,8,9]\d{8}", n) or \
                    re.match(r"147\d{8}|178\d{8}", n) or \
                    re.match(r"15[0,1,2,7,8,9]\d{8}", n) or \
                    re.match(r"18[2,3,4,7,8]\d{8}", n):
                # print("该号码属于：中国移动")
                return True
            else:
                # 中国电信
                # 133,153,180,181,189,177,173,149
                # print("该号码属于：中国电信")
                return True
        else:
            return False
    else:
        return False


def u_register(request):
    context = dict()
    if request.method == 'POST':
        newuser = UserRegister()

        # 验证手机号是否正确
        if isPhone_valid(request.POST['u_mobile']):
            u_mob_num = request.POST['u_mobile']
        else:
            context['error'] = "手机号错误"
            return render(request,'inner_register.html',context)
        newuser.account_number = u_mob_num

        # 两次密码不一致
        if request.POST['ur_pwd'] != request.POST['ur_cfmpwd']:
            context['error'] = "两次密码不一致"
            return render(request,'inner_register.html',context)
        else:
            newuser.password = make_password(request.POST['ur_pwd'])
        newuser.save()
        return HttpResponseRedirect(reverse('user:logintest'))
    else:
        return render(request,'inner_register.html')


def u_login(request):
    context = dict()
    if request.method == 'POST':
        mobile = request.POST['mobile']
        try:
            log_user = UserRegister.objects.get(account_number=mobile)
        except:
            context['ERROR_INFO'] = "账号或密码错误"
            return render(request,'inner_login.html',context)
        pwd = request.POST['password']
        if check_password(pwd, log_user.password):
            request.session["username"] = log_user.account_number
            mobile_num = request.session['username']
            user = UserRegister.objects.get(account_number=mobile_num)
            if user.times - new_messages.objects.filter(new_pub__year=datetime.datetime.now().year,new_pub__month=datetime.datetime.now().month).count() <= 0 :
                user.times = 0
            else:
                user.times = user.times - new_messages.objects.filter(new_pub__year=datetime.datetime.now().year,new_pub__month=datetime.datetime.now().month).count() <= 0
            user.save()
            return render(request,'main.html',{'login_flag':True})
        context['ERROR_INFO'] = '密码错误'
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request,'inner_login.html')


# 用户登录的时候要计算并更新剩余发布次数
def u_forget(request):
    context = dict()
    if request.method == 'POST':
        # 页面上发送验证码给手机，输入验证码进入重置密码的页面
        # 先用简单的试一试
        if not isPhone_valid(request.POST['u_mobile']):
            return render(request,'forgetpwd.html',{'error':'手机格式不正确'})
        try:
            chgpwd_user = UserRegister.objects.get(account_number=request.POST['u_mobile'])
        except:
            return render(request,'forgetpwd.html',{'error':'该手机号未注册'})

        # 这里需要判断验证码的东西
        return render(request,'resetpwd.html',{'username':request.POST['u_mobile']})
    else:
        return render(request,'forgetpwd.html')

def u_reset(request):
    if request.method == 'POST':
        chgpwd_user = UserRegister.objects.get(account_number=request.POST['username'])
        if request.POST['ur_pwd'] != request.POST['ur_cfmpwd']:
            return render(request,'resetpwd.html',{'error':'两次密码不一致'})
        else:
            chgpwd_user.password = make_password(request.POST['ur_pwd'])
            chgpwd_user.save()
        return HttpResponse("修改成功")
    else:
        return Http404