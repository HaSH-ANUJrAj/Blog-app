from cmath import e
import email
from multiprocessing import context
from django.conf import settings
from django.shortcuts import render , redirect
from .form import *
from django.contrib.auth import logout
from django.contrib import messages
from .models import *
import uuid
from django.core.mail import send_mail

from django.contrib.auth.models import User
import uuid
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required

# Create your views here.


def logout_view(request):
    logout(request)
    return redirect('/')


def home(request):
    context = {'blogs' : BlogModel.objects.all()}
    return render(request, 'home.html' , context)



def login_view(request):
    
    return render(request , 'login.html')

def register_view(request):
   
    return render(request , 'register.html')

def blog_detail(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug = slug).first()
        context['blog_obj'] = blog_obj

    except Exception as e:
        print(e)
    return render(request , 'blog_detail.html', context)
def see_blog(request):
    context = {}
    try:
        blog_objs = BlogModel.objects.filter(user = request.user)
        context['blog_objs'] = blog_objs
    except Exception as e:
        print(e)
    return render(request, 'see_blog.html', context)


def add_blog(request):
    context = {'form' : BlogForm}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user
            
            if form.is_valid():
                content = form.cleaned_data['content']
            
            blog_obj = BlogModel.objects.create(
                user = user , title = title, 
                content = content, image = image
            )
            print(blog_obj)
            return redirect('/add-blog/')

    except Exception as e:
        print(e)

    return render(request, 'add_blog.html',context)

def blog_update(request ,slug):
    context = {}
    try:
        
        blog_obj = BlogModel.objects.get(slug = slug)
        

        if blog_obj.user != request.user:
            return redirect('/')

        initial_dict ={'content' : blog_obj.content}
        form = BlogForm(initial=initial_dict)
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user
            
            if form.is_valid():
                content = form.cleaned_data['content']
            
            blog_obj = BlogModel.objects.create(
                user = user , title = title, 
                content = content, image = image
            )

        context['blog_obj'] =blog_obj
        context['form' ] = form



        
    except Exception as e:
        print(e)

    return render(request , 'update_blog.html', context)

def blog_delete(request ,id):
    try:
        blog_obj = BlogModel.objects.get(id = id)

        if blog_obj.user == request.user:
            blog_obj.delete()
    except Exception as e:
        print(e)

    return redirect('/see-blog/')


def verify(request , token):
    try:
        profile_obj = Profile.objects.filter(token = token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/register')
        else:
            return redirect('/register')
    except Exception as e:
        print(e)
        return redirect('/')

def success(request):
    return render(request , 'success.html')

def token_send(request):
    return render(request , 'token_send.html')

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )