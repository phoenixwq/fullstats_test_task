from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from posts.models import Post


class PostApiTestCase(TestCase):
    def setUp(self):
        self.u1 = get_user_model().objects.create_user(
            username="test_user",
            password="password"
        )

        self.u2 = get_user_model().objects.create_user(
            username="test_user2",
            password="password"
        )

        posts = [
            Post.objects.create(
                author=self.u1,
                article=1,
                title="Post 1 Title",
                overview="Post 1 overview",
                content="Post 1 Content",
            ),
            Post.objects.create(
                author=self.u2,
                article=2,
                title="Post 2 Title",
                overview="Post 2 overview",
                content="Post 2 Content",
            ),
        ]

        self.post_lookup = {p.id: p for p in posts}
        self.client = APIClient()
        self.client.login(username='test_user2', password='password')

    def test_post_list(self):
        resp = self.client.get("/api/v1/posts/")
        data = resp.json()["results"]
        self.assertEqual(len(data), 2)

        for post_dict in data:
            post_obj = self.post_lookup[post_dict["id"]]
            self.assertEqual(post_obj.title, post_dict["title"])
            self.assertEqual(post_obj.article, post_dict["article"])
            self.assertEqual(post_obj.overview, post_dict["overview"])
            self.assertEqual(post_obj.get_visits_count(), post_dict["visits"])
            self.assertEqual(post_obj.get_likes_count(), post_dict["likes"])
            self.assertEqual(post_obj.get_dislikes_count(), post_dict["dislikes"])

    def test_post_create(self):
        post_dict = {
            "title": "Test Post",
            "overview": "Post overview",
            "article": 4,
            "content": "Test Content",
        }
        resp = self.client.post("/api/v1/posts/", post_dict)
        post_id = resp.json()["id"]
        post_obj = Post.objects.get(pk=post_id)

        self.assertEqual(post_obj.title, post_dict["title"])
        self.assertEqual(post_obj.article, post_dict["article"])
        self.assertEqual(post_obj.overview, post_dict["overview"])
        self.assertEqual(post_obj.content, post_dict["content"])
