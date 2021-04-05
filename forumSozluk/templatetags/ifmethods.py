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
        myLikes = Like.objects.get(likeID=postID)
        if myLikes.likeAuthor == user.username:
            status = "true"
        else:
            status = "false"
    except:
        status = "false"
    return status