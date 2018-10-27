from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm, SignUpForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request,'blog/post_detail.html',{'post':post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.image = request.FILES['image']
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html',{'form':form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            # filepath = request.FILES.get('filepath', False)
            # if filepath != False:
            #     post.image = request.FILES['file']
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    posts_len = len(posts)
    return render(request, 'blog/post_draft_list.html',{'posts':posts,
    'posts_len':posts_len})

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def post_remove(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request,'blog/post_delete.html',{'post':post})

@login_required
def post_delete_confirm(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('post_list')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username = username, password=raw_password )
            login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()
    return render(request,'signup.html',{'form':form})


def author_detail(request,pk):
    user = request.user
    author = User.objects.get(pk=pk)
    posts = Post.objects.filter(author=author).order_by('-created_date')
    unpublishedCount = 0
    for post in posts:
        unpublishedCount += 1 if post.published_date is None else 0
    if user.pk == author.pk:
        return render(request,'blog/user_detail.html',{'author':author,
        'posts':posts,
        'unpublishedCount':unpublishedCount})
    else:
        return render(request,'blog/author_detail.html',{'author':author,
        'posts':posts})
