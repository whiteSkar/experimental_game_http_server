import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=256)
    date_published = models.DateTimeField()

    def __str__(self):
        return self.question_text

    def is_published_recently(self):
        return self.date_published >= timezone.now() - datetime.timedelta(days=1) 


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=128)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
