from django.contrib import admin
from django.urls import path,include
from .views import home,test,article_detail,PostCreateView,PostListView

urlpatterns = [
    path('test',test, name='test'),
    path('',home, name='home'),
    path('article/<int:post_id>/<slug:slug>/', article_detail, name='article_detail'),
     path('api/posts/', PostListView.as_view(), name='post-list'),
    path('api/posts/create/', PostCreateView.as_view(), name='post-create'),
]
