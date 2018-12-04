from django.core.paginator import Paginator
from django.shortcuts import render


from message.models import new_messages


# Create your views here.
def loadmore(request):
    list = new_messages.objects.order_by("new_pub")
    limit = 5
    paginor = Paginator(list,limit)
    page = request.GET.get('page',2)
    item_info = paginor.page(page)

    context = {'list':item_info,}
    template = 'main.html'
    return render(request, template, context)


# 主页需要显示一些东西
def home(request):
    context = dict()
    news = new_messages.objects.filter(new_type='A')
    policies = new_messages.objects.filter(new_type='B')
    hqs = new_messages.objects.filter(new_type='C')
    techs = new_messages.objects.filter(new_type='D')
    kxs = new_messages.objects.filter(new_type='E')
    if request.session.has_key('username'):
        login_flag = True
    else:
        login_flag = False
    context['news'] = news
    context['policies'] = policies
    context['hqs'] = hqs
    context['techs'] = techs
    context['login_flag'] = login_flag
    context['kxs'] = kxs
    return render(request, 'main.html', context)
