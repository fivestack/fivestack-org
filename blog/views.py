from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Post
from .forms import PostForm


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request=request, template_name='blog/post_list.html', context={'posts': posts, 'user': request.user})


def post_detail(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    return render(request=request, template_name='blog/post_detail.html', context={'post': post, 'user': request.user})


def post_new(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(to='post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request=request, template_name='blog/post_edit.html', context={'form': form})


def post_edit(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(data=request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect(to='post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request=request, template_name='blog/post_edit.html', context={'form': form, 'post': post})


def post_delete(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect(to='post_list')


def draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request=request, template_name='blog/post_draft_list.html', context={'posts': posts})


def post_publish(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect(to='post_detail', pk=pk)


def post_unpublish(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    post.unpublish()
    return redirect(to='post_detail', pk=pk)
