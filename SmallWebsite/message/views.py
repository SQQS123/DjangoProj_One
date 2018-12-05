import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

from user.views import my_login_required
from .models import new_messages
from user.models import UserRegister


# Create your views here.
def test(request):
    return HttpResponse("文章")


# 这里必须是登录用户,并且剩余发布次数不为零才能发布
@my_login_required
def fb(request):
    mobile_num = request.session['username']
    print(mobile_num)
    fb_user = UserRegister.objects.get(account_number=mobile_num)
    # 不如我们直接得到这个用户这个月发布的文章总数
    pubed_counts = new_messages.objects.filter(pub_user=fb_user).filter(new_pub__year=datetime.datetime.now().year).filter(
        new_pub__month=datetime.datetime.now().month).count()
    print(fb_user.level)
    if request.method == 'POST':
        if fb_user.level == 0:
            error = "VIP0无法发布,请充值"
            return render(request, 'messages/fb.html', {'login_flag': True, 'error': error})
        elif fb_user.level == 1:
            fb_user.times = 2 - pubed_counts
            if fb_user.times <= 0:
                error = "你当月额度已用尽，请升级"
                return render(request, 'messages/fb.html', {'login_flag': True, 'error': error})
        elif fb_user.level == 2:
            fb_user.times = 5 - pubed_counts
            if fb_user.times <= 0:
                error = "你当月额度已用尽，请升级"
                return render(request, 'messages/fb.html', {'login_flag': True, 'error': error})
        elif fb_user.level == 3:
            fb_user.times = 10 - pubed_counts
            if fb_user.times <= 0:
                error = "你当月额度已用尽"
                return render(request, 'messages/fb.html', {'login_flag': True, 'error': error})

        # 这里需要在数据库新建一条文章的内容
        new_message = new_messages()
        new_message.pub_user = fb_user

        # 保存到数据库
        new_message.new_title = request.POST['title']
        new_message.new_type= request.POST['type']
        new_message.new_detail = request.POST['detail']
        new_message.new_source = request.POST['source']
        new_message.new_auth = request.POST['author']
        new_message.new_img = request.FILES.get('uploadFile',None)
        new_message.save()
        fb_user.times = fb_user.times - 1
        fb_user.save()
        return render(request,'messages/fb_success.html')
    else:
        return render(request,'messages/fb.html', {'login_flag':True})


def showdetail(request,kind,article_id):
    try:
        mobile_num = request.session['username']
        login_flag = True
    except:
        login_flag = False
    context = dict()
    selected_news = new_messages.objects.get(id=article_id)
    context['news'] = selected_news
    context['login_flag'] = login_flag
    # 在这里可以点赞，评论，分享
    return render(request,'messages/detail.html',context)