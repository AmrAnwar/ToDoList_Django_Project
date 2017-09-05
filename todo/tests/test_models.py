from django.core.urlresolvers import reverse
from .test_init import InitTest
from ..models import List, Task, Sublist


class TestModels(InitTest):
    def setUp(self):
        super(TestModels, self).setUp()

    def test_sublist(self):
        self.assertEqual(str(self.sublist), "sublist sublist 2")