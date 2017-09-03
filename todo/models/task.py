# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from .list import List
from .helper import upload_location
from django.contrib.auth.models import User
from django.urls import reverse


# class TaskManager(models.Manager):
#     def active(self, *args, **kwargs):
#         """
#         filter archived objs or archived and specific user Lists
#         :param args:
#         :param kwargs:
#         :return: Queryset of lists filtered by archived element or archived and user
#         """
#         if 'user' in kwargs:
#             return super(TaskManager, self).filter(archived=False, user=kwargs['user'])


class Task(models.Model):
    """
    Task Model appears in List Detail and Has ModelViewSet
    """
    STATUS = (
        (1, 'NEW'),
        (2, 'READY'),
        (3, 'PROGRESS'),
        (4, 'DONE'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_tasks")
    list = models.ForeignKey(List, null=True, blank=True, related_name="list_tasks")
    assigned = models.ForeignKey(User, null=True, blank=True,
                                 related_name="assigned_tasks")

    title = models.CharField(null=False, blank=False, max_length=100)
    description = models.TextField(null=True, blank=True)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now_add=False,
                                       null=True, blank=True, default=None)
    file = models.FileField(upload_to=upload_location, null=True, blank=True)
    points = models.FloatField(default=0)
    status = models.IntegerField(choices=STATUS, default=1)

    # objects = TaskManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return "task %s" % self.title

    def get_absolute_url(self):
        return reverse("tasks-detail", kwargs={'pk': self.pk})
