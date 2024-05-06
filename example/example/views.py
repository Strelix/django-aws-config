from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from example import settings
from example.models import CatPictures, ProfilePictures


def index(request):
    created, user = User.objects.get_or_create(username="test")
    cat = CatPictures.objects.first()
    if request.user.is_authenticated:
        profile = ProfilePictures.objects.filter(user=request.user).first()
    else:
        profile = None

    return render(request, "index.html", {
        "public_image": profile.image if profile else None,
        "private_image": cat.image if cat else None,
    })


def login_view(request):
    if not request.method == "POST":
        return redirect("index")
    if request.user.is_authenticated:
        logout(request)
        return redirect("index")
    elif not request.user.is_authenticated:
        user, created = User.objects.get_or_create(username="test")

        login(request, user, backend="django.contrib.auth.backends.ModelBackend")

    return redirect("index")


def create_profile_picture(request):
    if request.method == "POST":
        profile = ProfilePictures.objects.first()
        if not profile:
            profile, created = ProfilePictures.objects.get_or_create(user=request.user)
        image = request.FILES.get("image")
        if image:
            profile.image = image
            profile.save()
    return redirect("index")


def create_cat_picture(request):
    if request.method == "POST":
        cat = CatPictures.objects.first()
        if not cat:
            cat = CatPictures.objects.create(user=request.user)
        image = request.FILES.get("image")
        if image:
            cat.image = image
            cat.save()
        else:
            cat.delete()
    return redirect("index")
