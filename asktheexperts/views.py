import os
from django import forms
from django.forms import ModelForm, ImageField, TextInput
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.db import IntegrityError
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, Http404, get_object_or_404
from django.urls import reverse

from .models import User, Question, Answer


class EditProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']


class ChangeImageForm(ModelForm):
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

    # Get answers count
    answers_count = Answer.objects.filter(question=question_id).count
    # Get answers from selected question
    answers = Answer.objects.filter(question=question_id, selected=False)
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


def select(request):
    # Mark answer as selected
    question_id = request.POST["question_id"]
    answer_id = request.POST["answer_id"]
    Answer.objects.filter(id=answer_id).update(selected=True)
    return HttpResponseRedirect(reverse("question",args=(question_id,)))


def unselect(request):
    # Unmark answer as selected
    question_id = request.POST["question_id"]
    answer_id = request.POST["answer_id"]
    Answer.objects.filter(id=answer_id).update(selected=False)
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
def change_photo(request):
    if request.method == 'POST':
        #form= ChangeImageForm(request.POST, request.FILES)
        #if form.is_valid():
        #    form.save()


        p_form = ChangeImageForm(request.POST,request.FILES,instance=request.user.user)
        if p_form.is_valid():
            photo = request.POST["photo"]
            User.objects.filter(id=request.user.id).update(photo=photo)
        #    p_form.photo = p_form.cleaned_data["photo"]
            #p_form.save()



#    if request.method == "POST":
#        form = ChangeImageForm(request.POST, instance=request.user)
#        if form.is_valid():
#            form.save()
#            if request.FILES.get('photo', None) != None:
#                try:
#                    os.remove(request.user.photo.url)
#                except Exception as e:
#                    print('Exception in removing old profile image: ', e)
#                request.user.photo = request.FILES['photo']
#                request.user.save()




#        update_profile_form = ChangeImageForm(data=request.POST, instance=user_profile)

#        if update_profile_form.is_valid():
#            profile = update_profile_form.save(commit=False)
#            profile.username = request.user.username

#            if 'photo' in request.FILES:
#                profile.photo = request.FILES['photo']

#            profile.save()





#    if request.method == "POST":
#        form = ChangeImageForm(request.POST)
#        user = get_object_or_404(user=request.user)
#        form = ChangeImageForm(request.POST, instance=["photo"])
#        if form.is_valid():
#            form.save()
            
        #if form.is_valid():
            
        #    new_photo = form.save(commit=False)
        #    new_photo.user = request.user
        #    new_photo.photo = form.cleaned_data["photo"]
            #new_photo.photo = new_photo.photo
        #    new_photo.save()
            
            #new_photo = form.save(commit=False)
            #new_photo.save(update_fields=['photo'])

            #User.objects.filter(id=request.user.id).update(photo=photo)
            return HttpResponseRedirect(reverse("settings"))

    else:
        return render(request, "asktheexperts/change_photo.html", {
            "form": ChangeImageForm(instance=request.user)
        })

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
