from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Users,Category,Comment,Desgin
import bcrypt


def index(request):
    return render(request,'index.html')


def register(request):
    if request.method == "POST":
        errors = Users.objects.validatorReg(request.POST)
        if errors:
            for value in errors.values():
                messages.error(request, value)
            return redirect('register')

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        new_user = Users.objects.create(
            username=username,
            email=email,
            password=pw_hash
        )

        request.session['user_id'] = new_user.id
        return redirect('index')

    return render(request, 'register.html')


def login(request):
    if request.method == "POST":
        errors = Users.objects.validatorLog(request.POST)
        if errors:
            for value in errors.values():
                messages.error(request, value)
            return redirect('login')

        matched_users = Users.objects.filter(email=request.POST['log_email'])
        if matched_users.exists():
            user = matched_users.first()
            if bcrypt.checkpw(request.POST['log_password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('index')
            else:
                messages.error(request, 'Invalid Password')
                return redirect('login')
        else:
            messages.error(request, 'Invalid Email')
            return redirect('login')

    return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return redirect("/")

#/////////////////////////////////////////////////////////////////
def profile(request, user_id):

    if "user_id" not in request.session:
        return redirect('login')
    profile_user = get_object_or_404(Users, id=user_id)
    
    context = {
        "user": profile_user,
        "user_id": user_id
    }
    return render(request, "profile.html", context)

def edit_profile(request, user_id):

    return render(request, "edit_profile.html")


def add_design(request, user_id):
    return render(request, "add_design.html")
#//////////////////////////////////////////////////////////////////////////////////


def design(request,num):
    design = Desgin.objects.get(id=num)
    comments=Comment.objects.all().order_by('-created_at')
    
    if request.method=='POST':
        text = request.POST.get('text')
        if request.session.get("Usersid"):
            Users = Users.objects.get(id=request.session['Usersid'])
            Comment.objects.create(text=text, Users=Users, design=design)
            return redirect('design_detail', design_id=num)
        
    likes_count = design.who_liked_it.count()
    liked_Userss = design.who_liked_it.all()
    liked_display = []
    if likes_count > 0:
        liked_display = [u.Usersname for u in liked_Userss[:2]]  
        others_count = likes_count - 2
    else:
        others_count = 0
    context = {        "design": design,
        "comments": comments,
        "likes_count": likes_count,
        "liked_display": liked_display,
        "others_count": others_count}
    return render(request,'design.html',context)

def new(request):
    if 'userid' not in request.session:
        return redirect('/')   
    
    categories = Category.objects.all()
    return render(request, 'upload.html', {'categories': categories})




def upload(request):
    if 'userid' not in request.session:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    if request.method == 'POST':
        errors = Desgin.objects.validatordes(request.POST, request.FILES)
        if errors:
            return JsonResponse({'errors': errors}, status=400)

        try:
            user = Users.objects.get(id=request.session['userid'])
        except Users.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        title = request.POST['title']
        category_id = request.POST['category']
        image = request.FILES.get('image')

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Invalid category'}, status=400)

        design = Desgin.objects.create(
            title=title,
            image=image,
            user_uploaded=user,
            category=category
        )

        return JsonResponse({
            'message': 'Design uploaded successfully',
            'design_id': design.id,
            'image_url': design.image.url if design.image else None
        })

    return JsonResponse({'error': 'Invalid request'}, status=405)


#///////////////////////////////////////////////////////////////
def category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    designs = Desgin.objects.filter(category=category)
    return render(request, 'category.html', {
        'category': category,
        'designs': designs
    })