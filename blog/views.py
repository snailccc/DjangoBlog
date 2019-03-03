from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from blog.models import Post

def index(request):
    posts = Post.objects.all().order_by('-create_time')
    return render(request,'blog/index.html',context={
        'post_list':posts
    })

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/detail.html',context={'post':post})

