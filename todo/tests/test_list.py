# from django.test import Client, TestCase
# from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
# from ..factories import ListFactory, TaskFactory, SubListFactory, UserFactory
#
#
# class TestMain(TestCase):
#     def setUp(self):
#
#         self.client = Client()
#         self.user = User(username="anwar")
#         self.user.set_password("password")
#         self.user.save()
#
#         self.user = User(username="guest")
#         self.user.set_password("password")
#         self.user.save()
#
#         self.list = ListFactory(user=self.user, users=(self.user,))
#         self.task = TaskFactory()
#         self.sublist = SubListFactory()
#
#     def test_lists_view(self):
#         self.client.login(username='anwar', password='password')
#         res = self.client.get(reverse('lists-list'))
#         self.assertEqual(res.status_code, 200)
#         res = self.client.get(self.list.get_absolute_url())
#
#         self.assertEqual(res.status_code, 200)
#         # login another account
#         self.client.login(username='guest', password='password')
#         self.assertEqual(self.client.get(reverse('lists-list')).status_code, 404)