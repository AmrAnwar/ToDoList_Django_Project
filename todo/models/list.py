# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from .helper import upload_location
from .project import Project


class List(models.Model):
    """
    the Project Model
    """
    project = models.ForeignKey(Project, related_name="project_lists", null=True)

    title = models.CharField(null=False, blank=False, max_length=100)
    description = models.TextField(null=True, blank=True)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=True)

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
        return "list:%s, pk:%s" % (self.title, self.pk)

    def get_absolute_url(self):
        """
        get detail url for List object
        :return: list detail url
        """
        return reverse("lists-detail", kwargs={'pk': self.pk})

    @property
    def get_progress(self):
        sum_total_points = 0
        sum_finished_points = 0
        for task in self.list_tasks.all():
            sum_total_points += task.points
            if task.status == 4:
                sum_finished_points += task.points
        if sum_total_points == 0: return 0
        return int((sum_finished_points / sum_total_points) * 100)

    def delete_url(self):
        return reverse("remove", kwargs={"pk": self.pk,
                                         "key": "list"})
