from django.test import Client, TestCase
from django.contrib.auth.models import User
from ..factories import ListFactory, TaskFactory, SubListFactory, ProfileFactory
from django.core.urlresolvers import reverse


class InitTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.amr = User(username="anwar", email="amr@example.com")
        self.amr.set_password("password")
        self.amr.save()

        self.user = User(username="guest")
        self.user.set_password("password")
        self.user.save()

        self.list = ListFactory(user=self.user, users=(self.user,))
        self.task = TaskFactory()
        self.sublist = SubListFactory()
        self.amr_profile = ProfileFactory(user=self.amr)
        self.new_profile = ProfileFactory()

    def test_home(self):
        self.assertEqual(self.client.get(reverse("home")).status_code,
                         200)
