from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .forms import PostForm, CommentForm


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request=request, template_name='blog/post_list.html', context={'posts': posts, 'user': request.user})


def post_detail(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    return render(request=request, template_name='blog/post_detail.html', context={'post': post, 'user': request.user})


@login_required
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


@login_required
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


@login_required
def post_delete(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect(to='post_list')


@login_required
def draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request=request, template_name='blog/draft_list.html', context={'posts': posts})


@login_required
def post_publish(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect(to='post_detail', pk=pk)


@login_required
def post_unpublish(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    post.unpublish()
    return redirect(to='post_detail', pk=pk)


def add_comment_to_post(request, pk: int):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(to='post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request=request, template_name='blog/add_comment_to_post.html', context={'form': form})


@login_required
def comment_approve(request, pk: int):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect(to='post_detail', pk=comment.post.pk)


@login_required
def comment_delete(request, pk: int):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect(to='post_detail', pk=comment.post.pk)
