from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import User, Question

def index(request):
    return render(request, "asktheexperts/index.html", {
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "asktheexperts/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "asktheexperts/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "asktheexperts/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "asktheexperts/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "asktheexperts/register.html")


def questions(request):
    questions = Question.objects.all().order_by("-timestamp")

    return render(request, "asktheexperts/questions.html", {
        "questions": questions
    })


@login_required(login_url="login")
def ask_question(request):
    if request.method == "GET":
        return render(request, "asktheexperts/ask_question.html")
    else:
        # Save new question
        title = request.POST["title"]
        content = request.POST["content"]
        new_question = Question(user=request.user, title=title, content=content)
        new_question.save()
        return HttpResponseRedirect(reverse("questions"))
