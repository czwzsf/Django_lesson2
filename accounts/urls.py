from django.urls import path

from accounts import views

urlpatterns = [
    path('user/info/', views.user_info, name='user_info'),
    path('user/list/slice/', views.user_list_slice, name='user_list_slice'),
    path('user/list/paginator/', views.user_list_paginator, name='user_list_paginator'),
    path('user/list/class/', views.UserListView.as_view(), name='user_list_class'),
]
