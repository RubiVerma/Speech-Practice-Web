from django.db import models
from django.contrib.auth.models import User

class SentenceRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sentence = models.TextField()
    spoken_text = models.TextField()
    accuracy = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.sentence[:30]}"

class PracticeSentence(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text[:50]
