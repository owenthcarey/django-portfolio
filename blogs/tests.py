import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Blog


class BlogModelTests(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_was_published_recently_with_future_blog(self):
        """
        was_published_recently() returns False for blogs whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_blog = Blog(
            title="Future blog",
            author=self.test_user,
            pub_date=time,
            content="Some content",
        )
        self.assertIs(future_blog.was_published_recently(), False)

    def test_was_published_recently_with_old_blog(self):
        """
        was_published_recently() returns False for blogs whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_blog = Blog(
            title="Old blog",
            author=self.test_user,
            pub_date=time,
            content="Some content",
        )
        self.assertIs(old_blog.was_published_recently(), False)

    def test_was_published_recently_with_recent_blog(self):
        """
        was_published_recently() returns True for blogs whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_blog = Blog(
            title="Recent blog",
            author=self.test_user,
            pub_date=time,
            content="Some content",
        )
        self.assertIs(recent_blog.was_published_recently(), True)


def create_blog(title: str, author: User, days: int, content: str = "") -> Blog:
    """
    Create a blog with the given `title` and `author` and published the
    given number of `days` offset to now (negative for blogs published
    in the past, positive for blogs that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Blog.objects.create(
        title=title, author=author, pub_date=time, content=content
    )


class BlogIndexViewTests(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_no_blogs(self):
        """
        If no blogs exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("blogs:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No blogs are available.")
        self.assertQuerySetEqual(response.context["latest_blog_list"], [])

    def test_past_blog(self):
        """
        Blogs with a pub_date in the past are displayed on the
        index page.
        """
        blog = create_blog(
            title="Past blog", author=self.test_user, days=-30, content="Some content"
        )
        response = self.client.get(reverse("blogs:index"))
        self.assertQuerySetEqual(
            response.context["latest_blog_list"],
            [blog],
        )

    def test_future_blog(self):
        """
        Blogs with a pub_date in the future aren't displayed on
        the index page.
        """
        create_blog(
            title="Future blog", author=self.test_user, days=30, content="Some content"
        )
        response = self.client.get(reverse("blogs:index"))
        self.assertContains(response, "No blogs are available.")
        self.assertQuerySetEqual(response.context["latest_blog_list"], [])

    def test_future_blog_and_past_blog(self):
        """
        Even if both past and future blogs exist, only past blogs
        are displayed.
        """
        blog = create_blog(
            title="Past blog", author=self.test_user, days=-30, content="Some content"
        )
        create_blog(
            title="Future blog", author=self.test_user, days=30, content="Some content"
        )
        response = self.client.get(reverse("blogs:index"))
        self.assertQuerySetEqual(
            response.context["latest_blog_list"],
            [blog],
        )

    def test_two_past_blogs(self):
        """
        The blogs index page may display multiple blogs.
        """
        blog1 = create_blog(
            title="Past blog 1", author=self.test_user, days=-30, content="Some content"
        )
        blog2 = create_blog(
            title="Past blog 2", author=self.test_user, days=-5, content="Some content"
        )
        response = self.client.get(reverse("blogs:index"))
        self.assertQuerySetEqual(
            response.context["latest_blog_list"],
            [blog2, blog1],
        )


class BlogDetailViewTests(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_future_blog(self):
        """
        The detail view of a blog with a pub_date in the future
        returns a 404 not found.
        """
        future_blog = create_blog(
            title="Future blog", author=self.test_user, days=5, content="Some content"
        )
        url = reverse("blogs:detail", args=(future_blog.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_blog(self):
        """
        The detail view of a blog with a pub_date in the past
        displays the blog's text.
        """
        past_blog = create_blog(
            title="Past blog", author=self.test_user, days=-5, content="Some content"
        )
        url = reverse("blogs:detail", args=(past_blog.id,))
        response = self.client.get(url)
        self.assertContains(response, past_blog.content)
