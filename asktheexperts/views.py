from django.core.mail import send_mail
import json
from django.http import JsonResponse
from django import forms
from django.core.paginator import Paginator
from django.forms import ModelForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.db import IntegrityError
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from .models import User, Question, Answer


# Form to change photo
class ChangePhotoForm(ModelForm):
    class Meta:
        model = User
        fields = ['photo']


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

        # Send a welcome email to the new registered user
        send_mail(
            'Subject here',
            'Here is the message.',
            'noreply@asktheexperts.com',
            ['to@example.com'],
            fail_silently=False,
        )

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "asktheexperts/register.html")


def questions(request):
    # Get all questions
    all_questions = Question.objects.all().order_by("-timestamp")

    # Add pagination
    paginator = Paginator(all_questions, 1)
    page_number = request.GET.get('page')
    questions = paginator.get_page(page_number)

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

    # Get answers count
    answers_count = Answer.objects.filter(question=question_id).count
    # Get answers from selected question
    answers = Answer.objects.filter(question=question_id, selected=False).order_by("-votes")
    # Get selected answers from selected question
    selected_answers = Answer.objects.filter(question=question_id, selected=True)
    
    return render(request, "asktheexperts/question.html", {
        "question": question,
        "answers": answers,
        "selected_answers": selected_answers,
        "answers_count": answers_count
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
    user_profile = User.objects.get(id=user_id)
    questions = Question.objects.filter(user_id=user_profile.id).order_by("-votes")
    return render(request, "asktheexperts/profile.html", {
        "user_profile": user_profile,
        "questions": questions
    })


@login_required(login_url="login")
def answer(request):
    # Save new answer
    question_id = request.POST["question_id"]
    new_answer = Answer(user_id=request.user.id, question_id=question_id, content=request.POST["content"])
    new_answer.save()
    return HttpResponseRedirect(reverse("question",args=(question_id,)))


@login_required()
def select(request):
    # Mark answer as selected
    question_id = request.POST["question_id"]
    answer_id = request.POST["answer_id"]
    Answer.objects.filter(id=answer_id).update(selected=True)

    # Update answer user's score
    answer_user_id = Answer.objects.get(id=answer_id).user_id
    answer_user_score = User.objects.get(id=answer_user_id).score
    new_score = answer_user_score + 15
    User.objects.filter(id=answer_user_id).update(score=new_score)

    # Update selector user score
    selector_score = User.objects.get(id=request.user.id).score
    new_score = selector_score + 2
    User.objects.filter(id=request.user.id).update(score=new_score)

    return HttpResponseRedirect(reverse("question",args=(question_id,)))


@login_required()
def unselect(request):
    # Unmark answer as selected
    question_id = request.POST["question_id"]
    answer_id = request.POST["answer_id"]
    Answer.objects.filter(id=answer_id).update(selected=False)
    return HttpResponseRedirect(reverse("question",args=(question_id,)))


@login_required(login_url="login")
def upvote_question(request):
    # Upvote question
    question_id = request.POST["question_id"]
    user = User.objects.get(id=request.user.id)
    user.upvote_question.add(question_id)
    user.downvote_question.remove(question_id)

    # Update votes number
    question = Question.objects.get(id=question_id)
    question.votes += 1
    question.save()

    # Update question user's score
    question_user_id = Question.objects.get(id=question_id).user_id
    question_user = User.objects.get(id=question_user_id)
    question_user.score += 10
    question_user.save()

    return HttpResponseRedirect(reverse("question",args=(question_id,)))


@login_required(login_url="login")
def downvote_question(request):
    # Downvote question
    question_id = request.POST["question_id"]
    user = User.objects.get(id=request.user.id)
    user.downvote_question.add(question_id)
    user.upvote_question.remove(question_id)

    # Update votes number
    question = Question.objects.get(id=question_id)
    question.votes -= 1
    question.save()

    # Update question user's score
    question_user_id = Question.objects.get(id=question_id).user_id
    question_user_score = User.objects.get(id=question_user_id).score
    new_score = question_user_score - 2
    if new_score < 1:
        new_score = 1
    User.objects.filter(id=question_user_id).update(score=new_score)

    return HttpResponseRedirect(reverse("question",args=(question_id,)))


@login_required(login_url="login")
def upvote_answer(request):
    # Upvote answer
    question_id = request.POST["question_id"]
    answer_id = request.POST["answer_id"]
    user = User.objects.get(id=request.user.id)
    user.upvote_answer.add(answer_id)
    user.downvote_answer.remove(answer_id)

    # Update votes number
    answer = Answer.objects.get(id=answer_id)
    answer.votes += 1
    answer.save()

    # Update answer user's score
    answer_user_id = Answer.objects.get(id=answer_id).user_id
    answer_user = User.objects.get(id=answer_user_id)
    answer_user.score += 10
    answer_user.save()

    return HttpResponseRedirect(reverse("question",args=(question_id,)))


@login_required(login_url="login")
def downvote_answer(request):
    # Downvote answer
    question_id = request.POST["question_id"]
    answer_id = request.POST["answer_id"]
    user = User.objects.get(id=request.user.id)
    user.upvote_answer.remove(answer_id)
    user.downvote_answer.add(answer_id)

    # Update votes number
    answer = Answer.objects.get(id=answer_id)
    answer.votes -= 1
    answer.save()

    # Update answer user's score
    answer_user_id = Answer.objects.get(id=answer_id).user_id
    answer_user_score = User.objects.get(id=answer_user_id).score
    new_score = answer_user_score - 2
    if new_score < 1:
        new_score = 1
    User.objects.filter(id=answer_user_id).update(score=new_score)

    # Update current user's score
    signed_in_user_score = User.objects.get(id=request.user.id).score
    new_score = signed_in_user_score - 1
    if new_score < 1:
        new_score = 1
    User.objects.filter(id=request.user.id).update(score=new_score)

    return HttpResponseRedirect(reverse("question",args=(question_id,)))


# FIXME: Maybe this can be removed
@login_required()
def report_user(request):
    if request.method == "POST":
        reported_user = request.POST["reported_user"]
        return render(request, "asktheexperts/report_user.html", {
            "reported_user": reported_user
        })


# FIXME: This looks better
@login_required()
def send_report(request):

    # Send report must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient reason
    # This is still part of version 1 and I'm not sure
    data = json.loads(request.body)
    emails = [email.strip() for email in data.get("reason").split(",")]
    if emails == [""]:
        return JsonResponse({
            "error": "At least one reason required."
        }, status=400)
    # ------------------------------------------------


    # Get contents of email
    reported_user = data.get("reportedUser", "")
    reason = data.get("reason", "")

    # Create one email for each recipient, plus sender
    # This version doesn't look the best
#    email = Email(
#        reported_useruser=reported_user,
#        reporting=request.user,
#        reason=reason,
#    )
#    email.save()
    # ------------------------------------------------


    # Another version ----------
#    post = Post.objects.get(id= post_id)
#    if data.get("reason") is not None:
#        post.content = data["reason"]
#        post.content = data["reason"]
#        post.save()
#    return HttpResponse(status=204)
    # --------------------------

    return JsonResponse({"message": "Email sent successfully."}, status=201)


@login_required(login_url="login")
def settings(request):
    # Render signed in user's settings page
    return render(request, "asktheexperts/account_info.html")


@login_required(login_url="login")
def change_photo(request):
    if request.method == 'POST':
        # Change user's profile photo
        form = ChangePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.photo = form.cleaned_data["photo"]
            form.save()
            return HttpResponseRedirect(reverse("settings"))
    else:
        return render(request, "asktheexperts/change_photo.html", {
            "form": ChangePhotoForm(instance=request.user)
        })


def remove_photo(request):
    # Replace user's profile photo with default photo
    user = User.objects.get(id=request.user.id)
    user.photo = 'images/default_image.jpg'
    user.save()
    return HttpResponseRedirect(reverse("settings"))


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
