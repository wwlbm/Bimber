from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(choices=Gender.choices)
    bio = models.TextField(null=True, blank=True)
    city = models.CharField(null=True, blank=True)
    photo = models.ImageField(upload_to="user/photos", blank=True, null=True)

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name="sent_messages", on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, related_name="received_messages", on_delete=models.CASCADE)
    message = models.CharField(default='You was liked')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

class Match(models.Model):
    from_user = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='matches_sent'
    )
    to_user = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='matches_received'
    )
    is_like = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        action = "like" if self.is_like else "dislike"
        return f"{self.from_user.username} {action} {self.to_user.username}"