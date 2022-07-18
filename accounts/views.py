from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from accounts.forms import LoginForm, UserEditForm
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


def user_register(request):
    """ 用户注册 """
    # 1. 获取表单的数据
    # 2. 验证数据是否符合要求
    # 3. 添加用户信息（用户基本信息、详细信息）
    username = '13000000002'
    try:
        user = User.objects.create(username=username,
                                   password='123456',
                                   nickname='王五')
        # profile = UserProfile.objects.create(user=user, username=username)
        profile = UserProfile.objects.create(user=user, usernamex=username)
        # 4. 反馈结果:成功/失败
        return HttpResponse('ok')
    except Exception as e:
        user.delete()
        print(e)
        return HttpResponse('no')


# 装饰器作用:如果上传上去的事务不满足数据库的要求，则不新建并回滚
@transaction.atomic()
def user_signup_trans(request):
    """ 事务的使用-装饰器 """
    username = '13000000003'
    user = User.objects.create(username=username,
                               password='123456',
                               nickname='王五')
    profile = UserProfile.objects.create(user=user, usernamex=username)
    return HttpResponse('ok')


def user_signup_trans_with(request):
    """ 事务的使用-with语法"""
    with transaction.atomic():
        username = '13000000005'
        user = User.objects.create(username=username,
                                   password='123456',
                                   nickname='王五')
        profile = UserProfile.objects.create(user=user, username=username)
    return HttpResponse('ok')


# @transaction.atomic()
def user_signup_trans_hand(request):
    """ 事务的自动提交 """
    username = '13000000007'
    # 放弃自动提交事务
    transaction.set_autocommit(False)
    try:
        user = User.objects.create(username=username,
                                   password='123456',
                                   nickname='王五')
        profile = UserProfile.objects.create(user=user, username=username)
        # profile = UserProfile.objects.create(user=user, usernamex=username)
        # 手动提交事务
        transaction.commit()
        # 4. 反馈结果:成功/失败
        return HttpResponse('ok')
    except Exception as e:
        # user.delete()
        print(e)
        # 手动控制事务，实现回滚
        transaction.rollback()
        return HttpResponse('no')


def user_login(request):
    """ 用户登录 """
    # form = LoginForm()
    # return render(request, 'user_login.html', {
    #     'form': form
    # })
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print('data:', data)
    else:
        form = LoginForm()
    return render(request, 'user_login.html', {
        'form': form
    })


def user_edit(request):
    """ 用户信息维护 """
    if request.method == 'POST':
        form = UserEditForm(data=request.POST)
        if form.is_valid():
            print('表单通过验证')
    else:
        form = UserEditForm()
    return render(request, 'user_edit.html', {
        'form': form
    })
