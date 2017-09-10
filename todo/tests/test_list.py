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

    # def test_form_valid(self):
    #     self.client.login(username='guest', password='password')
    #     data = {
    #         'title': 'mylist'
    #     }
    #     count = List.objects.count()
    #     self.client.post(reverse("lists-list"), data=data)
    #     self.assertEqual(count+1, List.objects.count())
