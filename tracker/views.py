from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from . models import Users, Projects
import bcrypt

# Create your views here.


def index(request):
    context = {
        'users': Users.objects.all(),
    }
    return render(request, "index.html", context)


def register(request):
    return render(request, 'register.html')


def register_user(request):
    errors = Users.objects.basic_validator(request.POST)

    # check username availability
    potential = request.POST["username"]
    username_scan = Users.objects.filter(username=potential)
    if len(username_scan) > 0:
        messages.error(request, "Username is already taken.")

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect("/register")

    else:
        hashed_pw = bcrypt.hashpw(
            request.POST["password"].encode(),
            bcrypt.gensalt()
        ).decode()

    newUser = Users.objects.create(
        username=request.POST['username'],
        password=hashed_pw
    )
    # if using user w/ email:
    # email = request.POST['email'],

    # add user id to session
    request.session['user_id'] = newUser.id
    return redirect('/')


def login_user(request):
    potential_user = Users.objects.filter(username=request.POST["username"])

    # verify username exists
    if len(potential_user) == 0:
        print("User not found")
        messages.error(
            request, "Please check your login credentials and try again.")

        return redirect('/')

    # if password matches
    if not bcrypt.checkpw(
        request.POST["password"].encode(),
        potential_user[0].password.encode()
    ):
        messages.error(
            request, "Please check your login credentials and try again.")

        return redirect("/")

    # successful log in
    request.session["user_id"] = potential_user[0].id
    return redirect("/dashboard")


def user_home(request):
    try:
        Users.objects.get(id=request.session['user_id'])
        is_logged_in = True
    except:
        is_logged_in = False

    context = {
        "is_logged_in": is_logged_in,
        "person": Users.objects.get(id=request.session['user_id']),
    }
    return render(request, 'index.html', context)
