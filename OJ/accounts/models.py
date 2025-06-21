from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserExtension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.CharField(max_length=100, blank=True)
    rank = models.IntegerField(default=0)
    problems_solved = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + " @ " + self.college
