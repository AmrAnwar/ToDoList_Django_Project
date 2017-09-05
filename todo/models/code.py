from django.db import models
from django.contrib.auth.models import User
from .list import List

import random
import string


class Code(models.Model):
    user = models.ForeignKey(User)
    list = models.ForeignKey(List)

    code = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.code = ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.digits) for _ in range(32))
        return super(Code, self).save(*args, **kwargs)
