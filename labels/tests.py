from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from labels.models import Label
from statuses.models import Status
from tasks.models import Task


class LabelsCrudTests(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.user = User.objects.get(username="user1")
        self.executor = User.objects.get(username="user2")
        self.label = Label.objects.create(name="bug")

    def test_labels_require_login(self):
        response = self.client.get(reverse("labels:list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])

    def test_create_label(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.post(reverse("labels:create"), data={"name": "feature"})
        self.assertRedirects(response, reverse("labels:list"))
        self.assertTrue(Label.objects.filter(name="feature").exists())

    def test_update_label(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.post(
            reverse("labels:update", args=[self.label.id]),
            data={"name": "ui"},
        )
        self.assertRedirects(response, reverse("labels:list"))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "ui")

    def test_delete_label(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.post(reverse("labels:delete", args=[self.label.id]))
        self.assertRedirects(response, reverse("labels:list"))
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())

    def test_cannot_delete_label_in_use(self):
        status = Status.objects.create(name="новый")
        task = Task.objects.create(
            name="Task with label",
            description="",
            status=status,
            author=self.user,
            executor=self.executor,
        )
        task.labels.add(self.label)

        self.client.login(username="user1", password="pass12345")
        response = self.client.post(
            reverse("labels:delete", args=[self.label.id]), follow=True
        )

        self.assertTrue(Label.objects.filter(id=self.label.id).exists())
        self.assertContains(
            response, "Невозможно удалить метку, потому что она используется"
        )
