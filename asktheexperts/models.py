from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    #photo = models.ImageField(default="/media/default_image.jpg",)
    #rank = models.IntegerField(default=1)
    
    #photo = models.FileField(upload_to='images/', null=True, verbose_name="")

    pass

class Question(models.Model):
    user = models.ForeignKey("User", on_delete=models.PROTECT, related_name="questioned")
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.title}"


class Answer(models.Model):
    user = models.ForeignKey("User", on_delete=models.PROTECT, related_name="answered_user")
    question = models.ForeignKey("Question", on_delete=models.PROTECT, related_name="answered_question")
    content = models.TextField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.user} answered {self.question}"


class Votes(models.Model):
    user = models.ForeignKey("User", on_delete=models.PROTECT, related_name="voted_user")
    question = models.ForeignKey("Question", on_delete=models.ProtectedError, related_name="question_voted")
    number_of_votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id} - {self.user} voted {self.question}"
    