from posts.models import Visit
from rest_framework.request import Request


def get_user_ip_address(request: Request) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def save_post_visit(request: Request, post):
    if request.session.session_key is None:
        request.session.save()
    session_key = request.session.session_key
    ip = get_user_ip_address(request)
    user_agent = request.headers.get('User-Agent', '')[:255]
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    visit = Visit.objects.get_or_create(
        post=post,
        user=user,
        ip=ip,
        user_agent=user_agent,
        session=session_key
    )
    return visit
