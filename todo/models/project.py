# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from .helper import upload_location


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_projects")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                   related_name="users_projects")
    title = models.CharField(max_length=30)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(
        upload_to=upload_location,
        null=True, blank=True,
        height_field='height_field',
        width_field='width_field',
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return "Project: %s" % self.title

    def get_absolute_url(self):
        """
        get detail url for List object
        :return: list detail url
        """
        return reverse("projects-detail", kwargs={'pk': self.pk})

    def delete_url(self):
        return reverse("remove", kwargs={"pk": self.pk,
                                         "key": "project"})

    @property
    def get_progress(self):
        if self.project_lists.count() == 0:
            return 0
        return sum([list.get_progress for list in self.project_lists.all()]) / self.project_lists.count()
