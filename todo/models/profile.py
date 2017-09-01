from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                       related_name="followers")

    def get_absolute_url(self):
        return reverse("accounts:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return "%s" % self.user

    @property
    def get_follow_instances(self):
        return self.followers.all()

    def get_follow_url(self):
        return reverse("accounts:follow_toggle", kwargs={"pk": self.pk})
