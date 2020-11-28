from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(upload_to='images/', default="images/default_image.jpg")
    upvote_question = models.ManyToManyField("Question", symmetrical=False, related_name="question_upvoted")
    upvote_answer = models.ManyToManyField("Answer", symmetrical=False, related_name="answer_upvoted")
    downvote_question = models.ManyToManyField("Question", symmetrical=False, related_name="question_downvoted")
    downvote_answer = models.ManyToManyField("Answer", symmetrical=False, related_name="answer_downvoted")
    score = models.IntegerField(default=1)
    joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.username}"


class Question(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="questioned")
    title = models.CharField(max_length=64)
    content = models.TextField(max_length=255)
    votes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.title}"


class Answer(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="answered_user")
    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="answered_question")
    content = models.TextField(max_length=255)
    votes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    selected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.user} answered {self.question}"


class Reported_User(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="reported_user")
    reason = models.TextField(max_length=255)
    solved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.user} - solved: {self.solved}"
