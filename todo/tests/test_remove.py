from django.core.urlresolvers import reverse
from .test_init import InitTest
from ..models import List, Task, Sublist, Project


class TestList(InitTest):
    def setUp(self):
        super(TestList, self).setUp()
        self.client.login(username="guest", password="password")

    def test_remove_project(self):
        count = Project.objects.count()
        self.client.delete(self.project.delete_url())
        self.assertEqual(count - 1, Project.objects.count())

    def test_remove_list(self):
        count = List.objects.count()
        self.client.delete(self.list.delete_url())
        self.assertEqual(count - 1, List.objects.count())

    def test_remove_task(self):
        count = Task.objects.count()
        self.client.delete(self.task.delete_url())
        self.assertEqual(count - 1, Task.objects.count())

    def test_remove_sublist(self):
        count = Sublist.objects.count()
        self.client.delete(self.sublist.delete_url())

        self.assertEqual(count - 1, Sublist.objects.count())

    def test_remove_wrong_key(self):
        res = self.client.delete(reverse("remove", kwargs={"pk": self.sublist.pk,
                                                           "key": "my_sublist"}))
        self.assertEqual(res.status_code, 404)
