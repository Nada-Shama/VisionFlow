from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import User,Category,Comment,Desgin
import bcrypt


def index(request):
    return render(request,'index.html')


# ----------------- REGISTER -----------------
def register(request):
    if request.method == "POST":
        errors = User.objects.validatorReg(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

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
        return redirect('dash')

    return render(request, 'register.html')

# ----------------- LOGIN -----------------
def login(request):
    if request.method == "POST":
        errors = User.objects.vaildatorlog(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

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


# ----------------- LOGOUT -----------------
def logout(request):
    request.session.flush()
    return redirect("/")
