from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from helper import upload_location
from PIL import Image as Img
import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class Profile(models.Model):
    """
    the user profile model to store the profile Image, followers
    """
    user = models.OneToOneField(User, related_name='profile')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                       related_name="followers")
    image = models.ImageField(
        upload_to=upload_location,
        null=True, blank=True,
    )

    about = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("profile-detail", kwargs={"username": self.user.username})

    def __str__(self):
        return "%s" % self.user

    def save(self, *args, **kwargs):
        """
        reduce the image quality
        :param args:
        :param kwargs:
        """
        if self.image:
            image = Img.open(StringIO.StringIO(self.image.read()))
            output = StringIO.StringIO()
            image.save(output, format='JPEG', quality=30)
            output.seek(0)
            self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name, 'image/jpeg',
                                              output.len, None)
        super(Profile, self).save(*args, **kwargs)
