from django import template
from forumSozluk.models import User
from forumSozluk.models import Post
from forumSozluk.models import Like
from django.http import HttpResponse

register = template.Library()

@register.filter
def ifmethods(postID,user):
    status = "none"
    try:
        likes = Like.objects.get(postAuthor=user.username,likeID=postID)
        print(likes.postAuthor+" Post Sahibiyiz!")
        print(likes.likeAuthor+" Beğenen")
        if likes.likeAuthor == user.username:
            status = "true"
            print("Beğendik")
        else:
            status = "false"
            print("Beğenmedik")
    except:
        likes = Like.objects.get(likeAuthor=user.username,likeID=postID)
        print(likes.likeAuthor + " Like Sahibiyiz!")
        print(likes.postAuthor + " Post Sahibi")
        if likes.likeAuthor == user.username:
            status = "true"
            print("Beğendik")
        else:
            status = "false"
            print("Beğenmedik")
    return status