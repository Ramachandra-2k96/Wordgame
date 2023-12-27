# models.py
from django.db import models
from django.contrib.auth.models import User
        
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=800)
    computer_response = models.CharField(max_length=800)
    time = models.DateTimeField(auto_now_add=True)
    user_score = models.IntegerField(default=0)
    computer_score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.content}'

