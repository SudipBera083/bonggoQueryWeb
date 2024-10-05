# models.py
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link message to user
    content = models.TextField(default="None")  # User's message content
    response = models.TextField(null=True, blank=True)  # Response content from the system
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp for when the message was created

    def __str__(self):
        return f'{self.user.username}: {self.content}'
