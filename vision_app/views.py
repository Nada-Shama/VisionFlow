from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Users,Category,Comment,Desgin
import bcrypt
from django.templatetags.static import static


def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')



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
    return redirect("login")

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
    if "user_id" not in request.session:
        return redirect("login")

    user = get_object_or_404(Users, id=user_id)

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        profile_picture = request.FILES.get("profile_picture")

        if username:
            user.username = username
        if email:
            user.email = email
        if profile_picture:
            user.profilepic = profile_picture

        user.save()
        return redirect("profile", user_id=user.id)

    return render(request, "edit_profile.html", {"user": user})



def add_design(request, user_id):
    if "user_id" not in request.session:
        return redirect("login")

    user = get_object_or_404(Users, id=user_id)   # safer than .get()
    categories = Category.objects.all() 

    if request.method == "POST":
        errors = Desgin.objects.validatordes(request.POST, request.FILES)
        if errors:
            return render(request, "add_design.html", {
                "categories": categories,
                "errors": errors,
                "profile_user": user   # <-- add this
            })

        title = request.POST.get("title")
        image = request.FILES.get("image")
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)

        Desgin.objects.create(
            title=title,
            image=image,
            category=category,
            user_uploaded=user
        )
        return redirect("profile", user_id=user.id)

    return render(request, "add_design.html", {
        "categories": categories,
        "profile_user": user  # <-- add this
    })



#//////////////////////////////////////////////////////////////////////////////////


def design(request, num):

    design = get_object_or_404(Desgin, id=num)
    comments = Comment.objects.filter(design=design).order_by('-created_at')

    likes_count = design.who_liked_it.count()
    liked_users = design.who_liked_it.all()
    liked_display = []
    if likes_count > 0:
        liked_display = [u.username for u in liked_users[:2]]
        others_count = likes_count - 2
    else:
        others_count = 0

    context = {
        "design": design,
        "comments": comments,
        "likes_count": likes_count,
        "liked_display": liked_display,
        "others_count": others_count
    }
    return render(request, 'design.html', context)


def add_comment(request, design_id):
    if request.method == "POST":
        if not request.session.get("user_id"):
            return JsonResponse({"error": "You must be logged in to comment."}, status=403)

        text = request.POST.get("comment_text")
        if not text:
            return JsonResponse({"error": "Comment cannot be empty."}, status=400)

        user = get_object_or_404(Users, id=request.session["user_id"])
        design = get_object_or_404(Desgin, id=design_id)

        comment = Comment.objects.create(
            text=text,
            user=user,
            design=design
        )

        profilepic_url = user.profilepic.url if user.profilepic else static('img/default.png')

        return JsonResponse({
            "username": user.username,
            "text": comment.text,
            "created_at": comment.created_at.strftime("%b %d, %Y %H:%M"),
            "profilepic": profilepic_url
        })
    return JsonResponse({"error": "Invalid request."}, status=400)



def new(request):
    if 'userid' not in request.session:
        return redirect('login')   
    
    categories = Category.objects.all()
    return render(request, 'upload.html', {'categories': categories})



def like_design(request, design_id):
    if "user_id" not in request.session:
        return JsonResponse({"error": "You must be logged in to like a design."}, status=403)

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method."}, status=400)

    design = get_object_or_404(Desgin, id=design_id)
    user = get_object_or_404(Users, id=request.session["user_id"])

    if user in design.who_liked_it.all():
        design.who_liked_it.remove(user)
        liked = False
    else:
        design.who_liked_it.add(user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes_count": design.who_liked_it.count()
    })


#///////////////////////////////////////////////////////////////
def category(request, category_id):

    category = get_object_or_404(Category, id=category_id)
    designs = Desgin.objects.filter(category=category)
    return render(request, 'category.html', {
        'category': category,
        'designs': designs
    })