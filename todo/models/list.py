# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from .helper import upload_location


class ListManager(models.Manager):
    def active(self, **kwargs):
        """
        filter archived objs or archived and specific user Lists
        :param args:
        :param kwargs:
        :return: Queryset of lists filtered by archived element or archived and user
        """
        if 'user' in kwargs:
            return super(ListManager, self).filter(archived=False, user=kwargs['user'])
        return super(ListManager, self).filter(archived=False)


class List(models.Model):
    """
    the List Model
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="user_lists")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                   related_name="users_lists")

    title = models.CharField(null=False, blank=False, max_length=100)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(
        upload_to=upload_location,
        null=True, blank=True,
        height_field='height_field',
        width_field='width_field',
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    objects = ListManager()

    class Meta:
        ordering = ["-created_at"]

    def __unicode__(self):
        return "list:%s, pk:%s" % (self.title, self.pk)

    @property
    def get_absolute_url(self):
        """
        get detail url for List object
        :return: list detail url
        """
        return reverse("lists-detail", kwargs={'pk': self.pk})
