from .test_init import InitTest


class TestList(InitTest):
    def setUp(self):
        super(TestList, self).setUp()

    def test_get_task(self):
        res = self.client.get(self.task.get_absolute_url())
        self.assertEqual(res.status_code, 404)
        self.client.login(username="anwar", password="password")
        res = self.client.get(self.task.get_absolute_url())
        self.assertEqual(res.status_code, 404)
        self.client.login(username="guest", password="password")
        res = self.client.get(self.task.get_absolute_url())
        self.assertEqual(res.status_code, 200)

    def test_update(self):
        self.client.login(username="guest", password="password")
        data = {
            "title": "test-title"
        }
        self.client.post(self.task.get_absolute_url(), data=data)

