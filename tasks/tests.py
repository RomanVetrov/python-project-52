from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from statuses.models import Status
from labels.models import Label
from tasks.models import Task


class TasksCrudTests(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.user1 = User.objects.get(username="user1")
        self.user2 = User.objects.get(username="user2")
        self.status = Status.objects.create(name="новый")
        self.status2 = Status.objects.create(name="в работе")
        self.label = Label.objects.create(name="bug")
        self.label2 = Label.objects.create(name="feature")
        self.task = Task.objects.create(
            name="Task 1",
            description="Desc",
            status=self.status,
            author=self.user1,
            executor=self.user2,
        )
        self.task.labels.add(self.label)
        self.other_task = Task.objects.create(
            name="Task 2",
            description="Another",
            status=self.status2,
            author=self.user2,
            executor=self.user1,
        )
        self.other_task.labels.add(self.label2)

    def test_guest_redirects_with_message(self):
        response = self.client.get(reverse("tasks:list"), follow=True)
        self.assertContains(response, "Вы не авторизованы! Пожалуйста, выполните вход.")
        self.assertEqual(response.resolver_match.view_name, "login")

    def test_create_task(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.post(
            reverse("tasks:create"),
            data={
                "name": "New task",
                "description": "Hello",
                "status": self.status.id,
                "executor": self.user2.id,
                "labels": [self.label.id],
            },
        )
        self.assertRedirects(response, reverse("tasks:list"))
        created = Task.objects.get(name="New task", author=self.user1)
        self.assertIn(self.label, created.labels.all())

    def test_update_task(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.post(
            reverse("tasks:update", args=[self.task.id]),
            data={
                "name": "Task 1 updated",
                "description": self.task.description,
                "status": self.status.id,
                "executor": self.user2.id,
                "labels": [self.label.id],
            },
        )
        self.assertRedirects(response, reverse("tasks:list"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Task 1 updated")

    def test_detail_task(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.get(reverse("tasks:detail", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task 1")
        self.assertContains(response, "bug")

    def test_filter_by_status(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.get(reverse("tasks:list"), {"status": self.status2.id})
        tasks = response.context["tasks"]
        self.assertEqual(list(tasks), [self.other_task])

    def test_filter_by_executor(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.get(reverse("tasks:list"), {"executor": self.user2.id})
        tasks = response.context["tasks"]
        self.assertIn(self.task, tasks)
        self.assertNotIn(self.other_task, tasks)

    def test_filter_by_label(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.get(reverse("tasks:list"), {"labels": self.label2.id})
        tasks = response.context["tasks"]
        self.assertEqual(list(tasks), [self.other_task])

    def test_filter_by_author_self(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.get(reverse("tasks:list"), {"self_tasks": "on"})
        tasks = response.context["tasks"]
        self.assertIn(self.task, tasks)
        self.assertNotIn(self.other_task, tasks)

    def test_only_author_can_delete_task(self):
        self.client.force_login(self.user2)  # <-- вместо login по паролю

        response = self.client.post(
            reverse("tasks:delete", args=[self.task.id]), follow=True
        )

        self.assertTrue(Task.objects.filter(id=self.task.id).exists())  # НЕ удалилось
        self.assertContains(response, "Только автор задачи может удалить её")

    def test_author_can_delete_task(self):
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse("tasks:delete", args=[self.task.id]), follow=True
        )

        self.assertRedirects(response, reverse("tasks:list"))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
