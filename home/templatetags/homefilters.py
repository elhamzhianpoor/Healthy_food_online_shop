from django import template
register = template.Library()


@register.filter(name='comlikechecker')
def com_like_checker(com,user):
    if com.liked_comment.filter(id=user.id).exists():
        return 'fa-solid'
    return 'fa-regular'


@register.filter(name='comdislikechecker')
def com_dislike_checker(com,user):
    if com.disliked_comment.filter(id=user.id).exists():
        return 'fa-solid'
    return 'fa-regular'
