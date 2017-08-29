import factory
from ..models import List
from django.contrib.auth.models import User


class ListFactory(factory.DjangoModelFactory):
    class Meta:
        model = List
    title = factory.sequence(lambda n: "list %s" % n)
    user = factory.Iterator(User.objects.all())
    image = factory.django.ImageField(color='red')

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if extracted:
            for user in extracted:
                self.users.add(user)
