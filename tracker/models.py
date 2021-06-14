from django.db import models
import re

from django.db.models.fields import CharField

# Create your models here.
# class UserManager(models.Manager):
#     def basic_validator(self, postData):
#         EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

#         errors = {}
#         if len(postData["username"]) < 2:
#             errors["username"] = "Username should be at least 2 characters"
#         if not EMAIL_REGEX.match(postData["email"]):
#             errors["email"] = "Please enter a valid email address"
#         if len(postData["password"]) < 5:
#             errors["password"] = "Please enter a password at least 5 characters long"
#         if postData["password"] != postData["confirmPW"]:
#             errors["confirmPW"] = "Please ensure both passwords match"
#         return errors

# class Users(models.Model):
#     username = models.CharField(max_length=80)
#     email = models.CharField(max_length=80)
#     password = models.CharField(max_length=80)
#     objects = UserManager()

# USER W/O EMAIL !!


class UserManager(models.Manager):
    def basic_validator(self, postData):

        errors = {}
        if len(postData["username"]) < 2:
            errors["username"] = "Username should be at least 2 characters."
        if len(postData["password"]) < 5:
            errors["password"] = "Please enter a password at least 5 characters long."
        if postData["password"] != postData["confirmPW"]:
            errors["confirmPW"] = "Please ensure both passwords match."
        return errors


class Users(models.Model):
    username = models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=80)
    objects = UserManager()


class Projects(models.Model):
    title = models.TextField(max_length=255, default="wip")
    # word_count = models.ListTextField(base_field=IntegerField(), size=200)
    word_count = models.IntegerField(default=0)
    deadline = models.DateTimeField(null=True, blank=True)
    desc = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    writer = models.ForeignKey(
        Users, related_name="author", on_delete=models.CASCADE)
