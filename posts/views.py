from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


def index(request):
    posts = Post.objects.all().order_by('-created_at')
    
    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'index.html', {'page_obj': page_obj})

def post(request, pk):
    posts = Post.objects.get(pk=pk)
    return render(request, 'posts.html', {'posts': posts})



def write(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.user
        
        post = Post(title=title, content=content, author=author)
        post.save()
        
        return redirect('/')
    
    return render(request, 'write.html')

def edit(request, pk):
    post = Post.objects.get(pk=pk)
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        
        post.save()
        
        return redirect(f'/post/{post.id}/')
    
    return render(request, 'edit.html', {'post': post})

def delete(request, pk):
    post = Post.objects.get(pk=pk)
    
    if request.user != post.author:
        messages.info(request, 'You are not authorized.')
        return redirect(f'/post/{post.id}/')
    else:
        post.delete()
    
    return redirect('profile')