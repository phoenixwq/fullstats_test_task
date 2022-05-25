from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

UserModel = get_user_model()


class Post(models.Model):
    article = models.PositiveIntegerField(
        db_index=True,
        unique=True
    )
    title = models.CharField(
        max_length=128,
        db_index=True
    )
    overview = models.CharField(max_length=256)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)
    author = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        related_name="posts",
        null=True
    )
    users_marks = models.ManyToManyField(
        UserModel,
        through="Mark",
        related_name="posts_marks"
    )
    users_visits = models.ManyToManyField(
        UserModel,
        through="Visit",
        related_name="posts_visits"
    )
    users_favorites = models.ManyToManyField(
        UserModel,
        through="Favorite",
        related_name="favorites_posts"
    )
    visits = models.PositiveIntegerField(default=0)

    @property
    def likes(self):
        return self.mark_set.filter(value=1).count()

    @property
    def dislikes(self):
        return self.mark_set.filter(value=-1).count()


class UserPostBase(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        UserModel,
        editable=False,
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        abstract = True
        unique_together = ["post", "user"]


class Mark(UserPostBase):
    value = models.IntegerField(
        validators=[MinValueValidator(-1),
                    MaxValueValidator(1)],
        default=0
    )


class Favorite(UserPostBase):
    pass


class Visit(UserPostBase):
    user = models.ForeignKey(
        UserModel,
        null=True,
        editable=False,
        on_delete=models.SET_NULL
    )
    ip = models.CharField(
        max_length=40,
        editable=False
    )
    session = models.CharField(
        max_length=40,
        editable=False
    )
    user_agent = models.CharField(
        max_length=255,
        editable=False
    )

    class Meta:
        pass
