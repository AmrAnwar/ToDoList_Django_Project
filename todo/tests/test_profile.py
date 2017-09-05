from .test_init import InitTest
from django.core.urlresolvers import reverse


class TestList(InitTest):
    def setUp(self):
        super(TestList, self).setUp()

    def test_view(self):
        self.client.login(username="anwar", password="password")
        res = self.client.get(reverse("profile-detail", kwargs={'username': self.amr_profile}))
        self.assertEqual(res.status_code, 200)
        data = {
            'email': "amr@example.com"
        }
        self.client.post(reverse("profile-detail", kwargs={'username': self.amr_profile}), data=data)
        self.assertEqual(self.amr_profile.user.email, "amr@example.com")
