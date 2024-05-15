from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from . models import Profile
from django.contrib import auth 
from .forms import ProfileForm



# Create your views here.

# 회원가입 
def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username = request.POST["username"],
                password = request.POST["password1"],
                email = request.POST["email"],
            )

            profile = Profile(
                user = user,
                nickname = request.POST["nickname"],

            )

            # 유저는 장고가 기본 제공하는 객체 
            # 프로필은 우리가 만든 객체이므로 저장을 해야함 
            profile.save()
            auth.login(request, user)
            
            return redirect("update_profile")

    return render(request, "users/signup.html")


# 로그인 
def login(request):
    if request.method == "POST": # 요청이 POST인지 
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None: # 유저가 있으면 
            auth.login(request, user)
            return redirect("home")
        else:
            return render(request, "users/login.html")
    return render(request, "users/login.html")


# 로그아웃
def logout(request):
    auth.logout(request)
    return redirect("home")




def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('home')  # 프로필 업데이트 후에 홈 페이지로 리디렉션
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/recommend.html', {'form': form})


def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/recommend.html', {'form': form})
