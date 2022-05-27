from celery.utils.log import get_task_logger
from celery import shared_task
from posts.models import Post
from django.db.models import Avg

logger = get_task_logger(__name__)


@shared_task
def posts_update():
    logger.info("start Posts update")
    posts = Post.objects.annotate(avg_mark=Avg("mark__value"))
    for post in posts:
        post.rating = post.avg_mark if post.avg_mark else 0
        post.visits = post.users_visits.count()
        post.save()
    logger.info("finish Posts update")
    return "Success"
