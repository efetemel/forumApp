from django import template
from forumSozluk.models import User
from forumSozluk.models import Post
from forumSozluk.models import Like
from django.http import HttpResponse

register = template.Library()

@register.filter
def smallStr(post):
    if len(post.content) >= 80:
        return post.content[0:80]
    else:
        return post.content