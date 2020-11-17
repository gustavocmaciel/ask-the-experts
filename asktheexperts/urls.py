from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("questions", views.questions, name="questions"),
    path("ask_question", views.ask_question, name="ask_question"),
    path("search", views.search, name="search"),
    path("profile/<int:user_id>/<str:username>", views.profile, name="profile"),
    path("questions/<int:question_id>", views.question, name="question"),
    path("answer", views.answer, name="answer"),
    path("select", views.select, name="select"),
    path("unselect", views.unselect, name="unselect"),
    path("upvote_question", views.upvote_question, name="upvote_question"),
    path("downvote_question", views.downvote_question, name="downvote_question"),
    path("upvote_answer", views.upvote_answer, name="upvote_answer"),
    path("downvote_answer", views.downvote_answer, name="downvote_answer"),
    path("settings", views.settings, name="settings"),
    path("settings/change-photo", views.change_photo, name="change_photo"),
    path("settings/remove-photo", views.remove_photo, name="remove_photo"),
    path("settings/change-username", views.change_username, name="change_username"),
    path("settings/change-email", views.change_email, name="change_email"),
    path("settings/change-password", views.change_password, name="change_password"),
    path("settings/delete-account", views.delete_account, name="delete_account")
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)