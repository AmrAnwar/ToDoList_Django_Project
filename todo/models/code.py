from django.db import models
from django.contrib.auth.models import User
from .project import Project

import random
import string


class Code(models.Model):
    """
    generate code related to specific user and list to invite this user to this list
    """
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project, null=True)

    code = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        """
        create the code field by using random strings and digits
        :param args:
        :param kwargs:
        """
        self.code = ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.digits) for _ in range(32))
        return super(Code, self).save(*args, **kwargs)
