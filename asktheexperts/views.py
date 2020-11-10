from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.db import IntegrityError
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from .models import User, Question, Answer


def index(request):
    return render(request, "asktheexperts/index.html")


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
                "message": "Invalid username and/or password."
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
    # Get all questions
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
    
    # Get question
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("Question not found.")

    # Get answers from selected question
    answers = Answer.objects.filter(question=question_id)
    
    return render(request, "asktheexperts/question.html", {
        "question": question,
        "answers": answers
    })


def search(request):
    # Search
    q = request.GET["q"]
    results = Question.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).order_by("-timestamp")
    return render(request, "asktheexperts/search_results.html", {
        "questions": results,
        "q": q

    })


def profile(request, user_id, username):
    # Render profile page from selected user
    user = User.objects.get(id=user_id)
    return render(request, "asktheexperts/profile.html", {
        "user": user
    })


@login_required(login_url="login")
def answer(request):
    # Save new answer
    question_id = request.POST["question_id"]
    new_answer = Answer(user_id=request.user.id, question_id=question_id, content=request.POST["content"])
    new_answer.save()
    return HttpResponseRedirect(reverse("question",args=(question_id,)))


def upvote_question(request):
    # Upvote question
    question_id = request.POST["question_id"]
    user = User.objects.get(id=request.user.id)
    user.vote_question.add(question_id)
    return HttpResponseRedirect(reverse("question",args=(question_id,)))


def downvote_question(request):
    # Downvote question
    question_id = request.POST["question_id"]
    user = User.objects.get(id=request.user.id)
    user.vote_question.remove(question_id)
    return HttpResponseRedirect(reverse("question",args=(question_id,)))


def upvote_answer(request):
    # Upvote answer
    question_id = request.POST["question_id"]
    answer_id = request.POST["answer_id"]
    user = User.objects.get(id=request.user.id)
    user.vote_answer.add(answer_id)
    return HttpResponseRedirect(reverse("question",args=(question_id,)))


def downvote_answer(request):
    # Downvote answer
    question_id = request.POST["question_id"]
    answer_id = request.POST["answer_id"]
    user = User.objects.get(id=request.user.id)
    user.vote_answer.remove(answer_id)
    return HttpResponseRedirect(reverse("question",args=(question_id,)))


@login_required(login_url="login")
def settings(request):
    # Render signed in user's settings page
    return render(request, "asktheexperts/account_info.html")


@login_required(login_url="login")
def change_username(request):
    # Change username
    if request.method == "POST":

        # Get new username
        new_username = request.POST["new_username"]

        # Get submited password
        submited_password = request.POST["password"]

        user = authenticate(request, username=request.user.username, password=submited_password)

        # If authentication successful, update username
        if user is not None:
            User.objects.filter(id=request.user.id).update(username=new_username)
            return HttpResponseRedirect(reverse("settings"))
        else:
            return render(request, "asktheexperts/change_username.html", {
                "message": "Invalid password."
            })
    else:
        return render(request, "asktheexperts/change_username.html", {
        })


@login_required(login_url="login")
def change_email(request):
    # Change email
    if request.method == "POST":

        # Get new email
        new_email = request.POST["new_email"]

        # Get submited password
        submited_password = request.POST["password"]

        user = authenticate(request, username=request.user.username, password=submited_password)

        # If authentication successful, update email
        if user is not None:
            User.objects.filter(id=request.user.id).update(email=new_email)
            return HttpResponseRedirect(reverse("settings"))
        else:
            return render(request, "asktheexperts/change_email.html", {
                "message": "Invalid password."
            })
    else:
        return render(request, "asktheexperts/change_email.html", {
        })


@login_required(login_url="login")
def change_password(request):
    # Change password
    if request.method == "POST":

        # Get new password
        new_password = request.POST["new_password"]

        # Get new confirmed password
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
        if new_password != confirmation:
            return render(request, "asktheexperts/change_password.html", {
                "message": "Passwords must match."
            })
        else:
            # Get current submited password
            submited_password = request.POST["password"]

            user = authenticate(request, username=request.user.username, password=submited_password)

            # If authentication successful, update password
            if user is not None:
                user = User.objects.get(id=request.user.id)
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                return HttpResponseRedirect(reverse("settings"))
            else:
                return render(request, "asktheexperts/change_password.html", {
                    "message": "Invalid password."
                })
    else:
        return render(request, "asktheexperts/change_password.html", {
    })


@login_required(login_url="login")
def delete_account(request):
    # Delete user's account
    if request.method == "POST":

        # Get password
        password = request.POST["password"]

        user = authenticate(request, username=request.user.username, password=password)
        # If authentication successful, delete account
        if user is not None:
            user = User.objects.get(id=request.user.id)
            user.delete()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "asktheexperts/change_password.html", {
                "message": "Invalid password."
            })
        pass
    else:
        return render(request, "asktheexperts/delete_account.html", {
        })
