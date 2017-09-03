from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from helper import upload_location


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                       related_name="followers")
    image = models.ImageField(
        upload_to=upload_location,
        null=True, blank=True,
    )

    about = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("accounts:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return "%s" % self.user

    def get_follow_instances(self):
        return self.following.all()

    def get_follow_url(self):
        return reverse("accounts:follow_toggle", kwargs={"pk": self.pk})
