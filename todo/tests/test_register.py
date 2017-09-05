from django.test import TestCase
from django.urls import reverse
from ..models import Profile

class RegisterViewTests(TestCase):

    def test_register_render(self):
        self.client.get(reverse('register'))

    def test_register_success(self):
        count = Profile.objects.count()
        data = {
            'first_name': "amr",
            'last_name': "anwar",
            'email': 'anwar@example.com',
            'username': 'amrlol',
            'about': "it's me ",
            'password': "password"
        }
        self.client.post(reverse('register'), data=data)
        self.assertEqual(count+1, Profile.objects.count())
