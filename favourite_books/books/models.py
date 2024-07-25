# books/models.py
from django.db import models

class MyUserManager(models.Manager):
    def create_user(self, email, password, first_name, last_name):
        if not email or not password or not first_name or not last_name:
            raise ValueError('All fields are required')
        user = self.create(email=email, password=password, first_name=first_name, last_name=last_name)
        return user

class MyUser(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    objects = MyUserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    uploaded_by = models.ForeignKey(MyUser, related_name='uploaded_books', on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(MyUser, related_name='favorite_books')
