from django.db import models
from accounts.models import UserExtension


# Create your models here.
class Problem(models.Model):
    title = models.CharField(max_length=100)
    statement = models.TextField()
    time_limit = models.IntegerField() # milliseconds
    space_limit = models.IntegerField() # megabytes
    tags = models.CharField(max_length=100) # CSV
    author = models.ForeignKey(UserExtension, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TestCase(models.Model):
    tc_number = models.IntegerField()
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_text = models.TextField()
    output_text = models.TextField()

    def __str__(self):
        return "TC" + str(self.tc_number) + "(" + self.problem.title + ")"


class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(UserExtension, on_delete=models.CASCADE)
    code = models.TextField()
    lang = models.CharField(max_length=50)
    verdict = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username + " " + self.verdict + " " + self.created_at
