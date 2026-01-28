from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class UsersCrudTests(TestCase):
    fixtures = ["users.json"]

    def test_create_user(self):
        url = reverse("users:create")
        response = self.client.post(
            url,
            data={
                "username": "newuser",
                "first_name": "New",
                "last_name": "User",
                "email": "new@example.com",
                "password1": "StrongPass12345",
                "password2": "StrongPass12345",
            },
        )
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_update_own_user(self):
        self.client.login(username="user1", password="pass12345")
        user = User.objects.get(username="user1")

        url = reverse("users:update", args=[user.id])
        response = self.client.post(
            url,
            data={
                "username": user.username,
                "first_name": "Changed",
                "last_name": user.last_name,
                "email": user.email,
            },
        )
        self.assertRedirects(response, reverse("users:list"))

        user.refresh_from_db()
        self.assertEqual(user.first_name, "Changed")

    def test_delete_own_user(self):
        self.client.login(username="user1", password="pass12345")
        user = User.objects.get(username="user1")

        url = reverse("users:delete", args=[user.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse("users:list"))
        self.assertFalse(User.objects.filter(id=user.id).exists())

    def test_cannot_update_other_user(self):
        self.client.login(username="user1", password="pass12345")
        other = User.objects.get(username="user2")

        url = reverse("users:update", args=[other.id])
        response = self.client.post(
            url,
            data={
                "username": other.username,
                "first_name": "Hacked",
                "last_name": other.last_name,
                "email": other.email,
            },
        )
        self.assertRedirects(response, reverse("users:list"))

        other.refresh_from_db()
        self.assertNotEqual(other.first_name, "Hacked")

    def test_login_redirects_to_index(self):
        url = reverse("login")
        response = self.client.post(
            url,
            data={
                "username": "user1",
                "password": "pass12345",
            },
        )
        self.assertRedirects(response, reverse("index"))

    def test_cannot_delete_user_with_tasks(self):
        self.client.login(username="user1", password="pass12345")
        user = User.objects.get(username="user1")
        status = Status.objects.create(name="новый")
        Task.objects.create(
            name="Task linked",
            description="",
            status=status,
            author=user,
        )

        url = reverse("users:delete", args=[user.id])
        response = self.client.post(url, follow=True)

        self.assertTrue(User.objects.filter(id=user.id).exists())
        self.assertContains(
            response,
            "Невозможно удалить пользователя, потому что он используется",
        )
