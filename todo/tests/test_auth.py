from .test_init import InitTest
from django.core.urlresolvers import reverse


class TestAuth(InitTest):
    def setUp(self):
        super(TestAuth, self).setUp()

    def test_login_render(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        self.client.login(username=self.amr.username, password='password')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_login_success(self):
        response = self.client.post(reverse('login'), data={
            'username': self.amr.username, 'password': 'password'})
        self.assertEqual(response.status_code, 302)

    def test_login_unsuccessful(self):
        response = self.client.post(reverse('login'), data={
            'username': self.amr.username, 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('login'), data={
            'username': 'wrong_amr', 'password': "password"})
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.amr.username, password="password")
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

