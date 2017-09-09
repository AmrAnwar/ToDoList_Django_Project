# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_projects")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                   related_name="users_projects")
    title = models.CharField(max_length=30)

    def __str__(self):
        return "Project: %s" % self.title
