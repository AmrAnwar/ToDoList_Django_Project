from django.core.urlresolvers import reverse
from .test_init import InitTest
from ..models import Code, Project


class TestProject(InitTest):
    def setUp(self):
        super(TestProject, self).setUp()

    def test_form_valid(self):
        self.client.login(username='guest', password='password')
        data = {
            'title': "TEST",
            'description': 'test',
        }
        count = Project.objects.count()
        res = self.client.post(reverse("projects-list"), data=data)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(count + 1, Project.objects.count())

    def test_update_project(self):
        self.client.login(username='guest', password='password')
        data = {
            'title': "TEST",
        }
        res = self.client.patch(self.project.get_absolute_url(), data=data)

    def test_project_lists(self):
        res = self.client.get(reverse("projects-list"))
        self.assertEqual(res.status_code, 302)
        self.client.login(username='guest', password='password')
        res = self.client.get(reverse("projects-list"))
        self.assertEqual(res.status_code, 200)

    def test_invite(self):
        code_obj = Code.objects.create(user=self.amr, project=self.project)
        self.assertEqual(code_obj.__str__(), self.amr.username)
        self.client.login(username='guest', password='password')
        res = self.client.get(reverse("projects-invite", kwargs={"code": code_obj.code}))
        self.assertEqual(res.status_code, 302)
        self.assertIn(self.amr, self.project.users.all())

    def test_invite_form(self):
        self.client.login(username='guest', password='password')
        count = Code.objects.count()
        data = {
            'prof1': "amr@example.com",
        }
        self.client.post(self.project.get_absolute_url(), data=data)
        self.assertEqual(Code.objects.count(), count + 1)
