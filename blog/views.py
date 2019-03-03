from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from blog.models import Post, Category
import markdown

def index(request):
    posts_list = Post.objects.all().order_by('-create_time')
    return render(request,'blog/index.html',context={
        'post_list':posts_list
    })

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/detail.html',context={'post':post})

def archives(request, year, month):
    date_list = Post.objects.filter(
        create_time__year = year,
        create_time__month = month
    ).order_by('-create_time')
    return render(request, 'blog/index.html',context={'date_list':date_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-create_time')
    return render(request,'blog/index.html',context={'post_list':post_list})