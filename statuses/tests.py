from django.test import TestCase
from django.urls import reverse

from statuses.models import Status


class StatusesCrudTests(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.status = Status.objects.create(name="новый")

    def test_statuses_requires_login(self):
        response = self.client.get(reverse("statuses:list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])

    def test_create_status(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.post(
            reverse("statuses:create"), data={"name": "в работе"}
        )
        self.assertRedirects(response, reverse("statuses:list"))
        self.assertTrue(Status.objects.filter(name="в работе").exists())

    def test_update_status(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.post(
            reverse("statuses:update", args=[self.status.id]),
            data={"name": "на тестировании"},
        )
        self.assertRedirects(response, reverse("statuses:list"))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "на тестировании")

    def test_delete_status(self):
        self.client.login(username="user1", password="pass12345")
        response = self.client.post(reverse("statuses:delete", args=[self.status.id]))
        self.assertRedirects(response, reverse("statuses:list"))
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())
