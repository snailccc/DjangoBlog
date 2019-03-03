from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView

import markdown

from blog.models import Post, Category

from comments.forms import CommentForm

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'


# def index(request):
#     posts_list = Post.objects.all()
#     return render(request,'blog/index.html',context={
#         'post_list':posts_list
#     })

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        respose = super(PostDetailView,self).get(request,*args,**kwargs)
        self.object.increase_views()
        return respose

    def get_object(self, queryset=None):
        post = super(PostDetailView,self).get_object(queryset=None)
        post.body = markdown.markdown(
            post.body,
            extension=[
                'markdown.extension.extra',
                'mark.extension.codehilite',
                'markdown.extension.toc',
            ]
        )
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView,self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form':form,
            'comment_list':comment_list
        })
        return context

# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     post.increase_views()
#
#     post.body = markdown.markdown(
#         post.body,
#         extensions=[
#             'markdown.extensions.extra',
#             'markdown.extensions.codehilite',
#             'markdown.extensions.toc'
#         ]
#     )
#     form = CommentForm()
#     comment_list = post.comment_set.all()
#     context = {
#         'post':post,
#         'form':form,
#         'comment_list':comment_list
#     }
#     return render(request, 'blog/detail.html',context=context)

class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView,self).get_queryset().filter(
            create_time__year=year,
            create_time__month=month,
        )

# def archives(request, year, month):
#     date_list = Post.objects.filter(
#         create_time__year = year,
#         create_time__month = month
#     )
#     return render(request, 'blog/index.html',context={'date_list':date_list})

class CategoryView(IndexView):

    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-create_time')
#     return render(request,'blog/index.html',context={'post_list':post_list})

