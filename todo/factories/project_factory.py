import factory
from ..models import Project
from django.contrib.auth.models import User


class ProjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = Project

    user = factory.Iterator(User.objects.all())

    title = factory.sequence(lambda n: "project %s" % n)
    description = factory.Faker('text')
    image = factory.django.ImageField(color='blue')

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if extracted:
            for user in extracted:
                self.users.add(user)
