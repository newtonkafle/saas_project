from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.


# login view
def login_view(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/home")
    return render(request, "auth/login.html", {})

# register view
def register_view(request):

    if request.method=="POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        conf_password = request.POST.get("conf_password")

        user_exists = User.objects.filter(username__iexact = username).exists()
        email_exists = User.objects.filter(email__iexact = email).exists()


        if not user_exists and email_exists:
            User.objects.create_user(username, email, password)
            print('Registration successful')
        else:
            print('username or email already exists in database')
    return render(request, "auth/register.html", {})