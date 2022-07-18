from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from accounts.models import User, UserProfile


def user_info(request):
    """ 用户详情-查询优化 """
    user = User.objects.get(pk=1)
    # profile_list = UserProfile.objects.all()
    profile_list = UserProfile.objects.all().select_related('user')

    # 使用SQL查询
    user_list = User.objects.raw('SELECT * FROM  `accounts_user`')
    return render(request, 'user_info.html', {
        'user': user,
        'profile_list': profile_list,
        'user_list': user_list
    })


def user_list_slice(request):
    """ 分页-使用切片 """
    """ 分页-使用切片 """
    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except:
        # 出现异常默认设置为第一页
        page = 1
    # 每页放多少条数据
    page_size = 10
    # user_list = User.objects.all()[0: 10]
    # user_list = User.objects.all()[10: 20]
    start = (page - 1) * page_size
    end = page * page_size
    user_list = User.objects.all()[start: end]
    return render(request, 'user_list_slice.html', {
        'user_list': user_list
    })


def user_list_paginator(request):
    """ 分页-使用分页器 """
    page = request.GET.get('page', 1)
    user_list = User.objects.all()
    # 第一步，取得分页器
    p = Paginator(user_list, 15)
    # 第二步，取得某一页的对象（实例）
    # page_data = p.get_page(page)
    try:
        page_data = p.page(page)
    except EmptyPage as e:
        print('页面不存在')
        raise Http404
    except PageNotAnInteger as e:
        print('无效的页码')
        raise Http404

    return render(request, 'user_list_paginator.html', {
        'page_data': page_data
    })


class UserListView(ListView):
    """ 分页处理, 面向对象 """
    # 对应的模板
    template_name = 'user_list_class.html'
    # 对应的ORM模型
    model = User
    # 页面大小
    paginate_by = 20
    # 获取页面的参数（当期第几页）
    page_kwarg = 'p'

