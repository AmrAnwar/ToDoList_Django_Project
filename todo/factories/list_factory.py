import factory
from ..models import List, Project
from django.contrib.auth.models import User


class ListFactory(factory.DjangoModelFactory):
    class Meta:
        model = List
    project = factory.Iterator(Project.objects.all())

    title = factory.sequence(lambda n: "list %s" % n)
    image = factory.django.ImageField(color='red')

