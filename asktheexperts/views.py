from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from .models import User, Question, Answer

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


def question(request, question_id):
    
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Listing not found.")

    answers = Answer.objects.filter(question=question_id)

    
    return render(request, "asktheexperts/question.html", {
        "question": question,
        "answers": answers
    })


def profile(request, user_id, username):
    pass


@login_required(login_url="login")
def answer(request):
    # Save new answer
    question_id = request.POST["question_id"]
    new_answer = Answer(user_id=request.user.id, question_id=question_id, content=request.POST["content"])
    new_answer.save()
    return HttpResponseRedirect(reverse("question",args=(question_id,)))
