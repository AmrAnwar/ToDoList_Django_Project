# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from .task import Task
from django.urls import reverse

# Create your models here.


class Sublist(models.Model):
    """
    Sublist Model appears in Task Detail
    """
    task = models.ForeignKey(Task, related_name="task_sublist")

    title = models.CharField(null=False, blank=False, max_length=100)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return "sublist %s" % self.title

    def delete_url(self):
        return reverse("remove", kwargs={"pk": self.pk,
                                         "key": "sublist"})
