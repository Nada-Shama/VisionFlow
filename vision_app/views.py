from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import User,Category,Comment,Desgin
import bcrypt


def index(request):
    return render(request,'index.html')


def register(request):
    if request.method == "POST":
        errors = User.objects.validatorReg(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('register')

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        c_password = request.POST['c_password']

        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            username=username,
            email=email,
            password=pw_hash
        )

        # Save session
        request.session['userid'] = new_user.id
        return redirect('login')

    return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        errors = User.objects.validatorLog(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('login')

        user = User.objects.filter(email=request.POST['log_email'])
        if user:
            log_user = user[0]
            if bcrypt.checkpw(request.POST['log_password'].encode(), log_user.password.encode()):
                request.session['userid'] = log_user.id
                return redirect('index')
            else:
                messages.error(request, 'Invalid Password')
                return redirect('/')
        else:
            messages.error(request, 'Invalid Email')
            return redirect('/')
    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return redirect("/")


def profile(request):
    return render(request,'profile.html')

def design(request,num):
    design = Desgin.objects.get(id=num)
    comments=Comment.objects.all().order_by('-created_at')
    
    if request.method=='POST':
        text = request.POST.get('text')
        if request.session.get("userid"):
            user = User.objects.get(id=request.session['userid'])
            Comment.objects.create(text=text, user=user, design=design)
            return redirect('design_detail', design_id=num)
        
    likes_count = design.who_liked_it.count()
    liked_users = design.who_liked_it.all()
    liked_display = []
    if likes_count > 0:
        liked_display = [u.username for u in liked_users[:2]]  
        others_count = likes_count - 2
    else:
        others_count = 0
    context = {        "design": design,
        "comments": comments,
        "likes_count": likes_count,
        "liked_display": liked_display,
        "others_count": others_count}
    return render(request,'design.html',context)