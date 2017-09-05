import random


from django.core.urlresolvers import reverse
from .test_init import InitTest
from ..models import List, Task, Code


class TestList(InitTest):
    def setUp(self):
        super(TestList, self).setUp()

    def test_lists_view(self):
        self.assertEqual(self.client.get(reverse('lists-list')).status_code, 302)
        res = self.client.get(self.list.get_absolute_url())
        self.assertEqual(res.status_code, 404)

        self.client.login(username='guest', password='password')
        res = self.client.get(reverse('lists-list'))
        self.assertEqual(res.status_code, 200)
        res = self.client.get(self.list.get_absolute_url())
        self.assertEqual(res.status_code, 200)

    def test_form_valid(self):
        self.client.login(username='guest', password='password')
        data = {
            'title': 'mylist'
        }
        count = List.objects.count()
        self.client.post(reverse("lists-list"), data=data)
        self.assertEqual(count+1, List.objects.count())

    def test_invite(self):
        code_obj = Code.objects.create(user=self.amr, list=self.list)
        self.assertEqual(code_obj.__str__(), self.amr.username)
        self.client.login(username='guest', password='password')
        res = self.client.get(reverse("lists-invite", kwargs={"code": code_obj.code}))
        self.assertEqual(res.status_code, 302)
        self.assertIn(self.amr, self.list.users.all())

    def test_invite_form(self):
        self.client.login(username='guest', password='password')
        count = Code.objects.count()
        data = {
            'prof1': "amr@example.com",
        }
        self.client.post(self.list.get_absolute_url(), data=data)
        self.assertEqual(Code.objects.count(), count+1)