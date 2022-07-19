import random
from django.core.mail import EmailMessage
import requests,json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout


def intro(request):
    data = Problems.objects.all()[:3]
    return render(request,'intro.html',{"data":data})

@login_required
def homePage(request):
    return render(request,'index.html')

@login_required
def about(request):
    return render(request,'about.html')

@login_required
def contact(request):
    return render(request,'contact.html')


def signup(request):
    context={}
    if request.method=='POST':
        captcha_token = request.POST['g-recaptcha-response']
        captcha_url = "https://www.google.com/recaptcha/api/siteverify"
        captcha_secter = '6Le-0PYgAAAAAJ0YKMcEzXGyA6xaBmDzjLJtk8Pt'
        captcha_data = {"secret":captcha_secter, "response":captcha_token,}
        captcha_server_response = requests.post(url = captcha_url, data = captcha_data)
        captcha_json = json.loads(captcha_server_response.text)
        if captcha_json['success'] == False:
            context['dbresponse'] = 'Invalid reCaptcha !!!'
            context['error'] = 'alert-danger'
        else:
            username = request.POST['username']
            lname = request.POST['lname']
            fname = request.POST['fname']
            email = request.POST['email']
            pwd = request.POST['password1']
            usr = User.objects.create_user(email=email, password=pwd, username=username)
            usr.first_name=fname
            usr.last_name=lname
            usr.save()
            login(request,usr)
            response = redirect('/home')
            return response
    else:
        print('error')
    return render(request,'signup.html',context)

def login_page(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home-page')
        else:
            status = 'Password or Username incorrect !!!'
            col = 'alert alert-danger'
            context = {"status": status, "col": col}
            return render(request, 'login.html', context)
    return render(request,'login.html')


def logout_page(request):
    logout(request)
    return redirect('intro-page')
@login_required
def feedbacks(request):
    data = Problems.objects.all()
    context = {"data":data}
    return render(request,'feedback.html',context)

@login_required
def prob_detail(request,slug):
    data = get_object_or_404(Problems, slug=slug)
    context={"data":data}
    return render(request,'p_detail.html',context)


def check_user(request):
    username = request.GET['usern']
    check = User.objects.filter(username=username)
    if len(check)>0:
        return HttpResponse('Exists')
    else:
        return HttpResponse('No Exists')

@login_required
def new_feed(request):
    context={}
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        data = Feedback(author = request.user, title = title, text = text)
        data.save()
        context['status'] = 'Feedback has been created. Expect an answer soon.'
        context['col'] = 'alert-success'
    return render(request,'new_f.html',context)


def forgot_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        npwd = request.POST['newPwd']
        user = get_object_or_404(User, username=username)
        user.set_password(npwd)
        user.save()
        return redirect('intro-page')
    return render(request,'forgot_password.html')


def reset_password(request):
    username = request.GET['username']
    try:
        user = get_object_or_404(User, username=username)
        otp = random.randint(100000,999999)
        msg = f'Dear {user.first_name}, a one time code {otp} - has been sent to your mail. \nPlease do not give this code to anyone. \nBest Regards, NITS Team'
        try:
            em = EmailMessage('Reset Password',msg,to=[user.email])
            em.send()
            return JsonResponse({"status":'sent','email':user.email, "otp":otp})
        except:
            return JsonResponse({"status":'failed','email':user.email})
    except:
        return JsonResponse({"status":'error'})


@login_required
def profile(request):
    context = {}
    data = get_object_or_404(User, username=request.user)
    context['data'] = data
    return render(request,'profile.html',context)

@login_required
def edit_profile(request):
    data = get_object_or_404(User, username=request.user)
    if request.method=='POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['uname']
        email = request.POST['email']
        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()
        status = 'Your Profile successfully edited !!!'.title()
        return render(request,'edit_profile.html',{"status":status})


    return render(request,'edit_profile.html',{"data":data})



@login_required
def my_questions(request):
    context = {}
    data = Feedback.objects.filter(author = request.user)
    context['data'] = data
    return render(request,'questions.html',context)

@login_required
def feed_delete(request, pk):
    data = Feedback.objects.get(id=pk).delete()
    return redirect('question-page')


@login_required
def feed_update(request, pk):
    context={}
    data=Feedback.objects.get(id=pk)
    context['data']=data
    if request.method=='POST':
        title = request.POST['title']
        text= request.POST['text']
        Feedback.objects.filter(id=pk).update(title=title, text=text)
        return redirect('question-page')
    return render(request,'edit_feedback.html',context)



def error_404(request,exception):
    return render(request,'myapp/error404.html')
