from django.db import models

class User(models.Model):
    userID = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    photo = models.FileField(null=True, blank=True, upload_to="Images/")
    fullname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birtdate = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    last_join = models.CharField(max_length=255)
    about = models.CharField(max_length=255)
    me_flow = models.CharField(max_length=255) #bizim takip ettiklerimiz
    flow = models.CharField(max_length=255) #bizi takip edenler
    
class Meta:
    model = User
    fields = ("__all__")

class Post(models.Model):
    postID = models.CharField(max_length=255)
    postPreview = models.CharField(max_length=500)
    category = models.CharField(max_length=255)
    content = models.CharField(max_length=500)
    author = models.CharField(max_length=255)
    publish_date = models.CharField(max_length=255)
    like_count = models.CharField(max_length=255)


class ForgotPassword(models.Model):
    passwordID = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=255)


class Like(models.Model):
    likeID = models.CharField(max_length=255)
    postAuthor = models.CharField(max_length=255)
    likeAuthor = models.CharField(max_length=255)
    likeDate = models.CharField(max_length=255)

class Category(models.Model):
    categoryID = models.CharField(max_length=255)
    categoryName = models.CharField(max_length=255)
    categoryCount = models.CharField(max_length=255)