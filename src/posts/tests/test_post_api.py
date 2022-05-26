from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from posts.models import Post


class PostApiTestCase(APITestCase):
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

    def test_post_list_auth_user(self):
        resp = self.client.get("/api/v1/posts/")
        data = resp.json()["results"]
        self.assertEqual(len(data), 2)

        for post_dict in data:
            post_obj = self.post_lookup[post_dict["id"]]
            self.assertEqual(post_obj.title, post_dict["title"])
            self.assertEqual(post_obj.article, post_dict["article"])
            self.assertEqual(post_obj.overview, post_dict["overview"])
            self.assertEqual(post_obj.visits, post_dict["visits"])
            self.assertEqual(post_obj.likes, post_dict["likes"])
            self.assertEqual(post_obj.dislikes, post_dict["dislikes"])

    def test_post_list_anon_user(self):
        self.client.logout()
        resp = self.client.get("/api/v1/posts/")
        data = resp.json()["results"]
        self.assertEqual(len(data), 2)

        for post_dict in data:
            post_obj = self.post_lookup[post_dict["id"]]
            self.assertEqual(post_obj.title, post_dict["title"])
            self.assertEqual(post_obj.article, post_dict["article"])
            self.assertEqual(post_obj.overview, post_dict["overview"])
            self.assertEqual(post_obj.visits, post_dict["visits"])
            self.assertEqual(post_obj.likes, post_dict["likes"])
            self.assertEqual(post_obj.dislikes, post_dict["dislikes"])

    def test_post_create_auth_user(self):
        post_dict = {
            "title": "Test Post",
            "overview": "Post overview",
            "article": 4,
            "content": "Test Content",
        }
        resp = self.client.post("/api/v1/posts/", post_dict)
        post_id = resp.json()["id"]
        post_obj = Post.objects.get(pk=post_id)

        for k, v in post_dict.items():
            self.assertEqual(
                getattr(post_obj, k), v
            )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Post.objects.count(), 3)

    def test_post_create_anon_user(self):
        post_dict = {
            "title": "Test Post",
            "overview": "Post overview",
            "article": 4,
            "content": "Test Content",
        }
        self.client.logout()
        resp = self.client.post("/api/v1/posts/", post_dict)
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(Post.objects.count(), 2)

    def test_author_update_post(self):
        post_dict = {
            "title": "Test Post",
            "overview": "Post overview",
            "content": "Test Content",
        }
        posts = Post.objects.filter(author=self.u2)
        for index, post in enumerate(posts):
            post_dict["article"] = index + 10
            resp = self.client.put(f"/api/v1/posts/{post.pk}/", post_dict)
            update_post = Post.objects.get(pk=post.pk)
            for attr, value in post_dict.items():
                self.assertEqual(
                    getattr(update_post, attr), value
                )
            self.assertEqual(resp.status_code, 200)

    def test_not_author_update_post(self):
        post_dict = {
            "title": "Test Title - new",
            "overview": "Post overview - new",
            "content": "Test Content- new",
        }
        posts = Post.objects.filter(author=self.u2)
        self.client.login(username="test_user", password="password")
        for index, post in enumerate(posts):
            post_dict["article"] = index + 10
            resp = self.client.put(f"/api/v1/posts/{post.pk}/", post_dict)
            self.assertEqual(resp.status_code, 403)

    def test_anon_user_update_post(self):
        post_dict = {
            "title": "Test Title - new",
            "overview": "Post overview - new",
            "content": "Test Content- new",
        }
        posts = Post.objects.filter(author=self.u2)
        self.client.logout()
        for index, post in enumerate(posts):
            post_dict["article"] = index + 10
            resp = self.client.put(f"/api/v1/posts/{post.pk}/", post_dict)
            self.assertEqual(resp.status_code, 403)

    def test_author_delete_post(self):
        posts = Post.objects.filter(author=self.u2)
        for post in posts:
            resp = self.client.delete(f"/api/v1/posts/{post.pk}/")
            self.assertEqual(resp.status_code, 204)
        count_user_posts = Post.objects.filter(author=self.u2).count()
        self.assertEqual(count_user_posts, 0)

    def test_not_author_delete_post(self):
        posts = Post.objects.filter(author=self.u2)
        current_count = Post.objects.filter(author=self.u2).count()
        self.client.login(username="test_user", password="password")
        for post in posts:
            resp = self.client.delete(f"/api/v1/posts/{post.pk}/")
            self.assertEqual(resp.status_code, 403)
        new_count = Post.objects.filter(author=self.u2).count()
        self.assertEqual(current_count, new_count)

    def test_anon_user_delete_post(self):
        posts = Post.objects.filter(author=self.u2)
        current_count = Post.objects.filter(author=self.u2).count()
        self.client.logout()
        for post in posts:
            resp = self.client.delete(f"/api/v1/posts/{post.pk}/")
            self.assertEqual(resp.status_code, 403)
        new_count = Post.objects.filter(author=self.u2).count()
        self.assertEqual(current_count, new_count)
