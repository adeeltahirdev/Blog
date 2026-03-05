from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from posts.models import Post

# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already taken')
            return redirect('register')       
        
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email already registered')
            return redirect('register')
        
        else:
            user = User.objects.create_user(username=username, email=email, password=password)    
            user.save()
            messages.info(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        return render(request, 'register.html')
    
def login(request):
    if request.method == 'POST':    
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(username=username, password=password)
    
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def profile(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    paginator = Paginator(user_posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'profile.html', {'page_obj': page_obj})