from django import template
from forumSozluk.models import User
from forumSozluk.models import Post
from forumSozluk.models import Like
from django.http import HttpResponse

register = template.Library()

@register.filter
def contextStr(post):
    if len(post.content) >= 200:
        return post.content[0:200]+"..."
    else:
        return post.content