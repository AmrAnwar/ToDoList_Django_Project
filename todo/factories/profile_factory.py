import factory
import factory.fuzzy

from .user_factory import UserFactory
from ..models import Profile


class ProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    image = factory.django.ImageField(color='blue')
    about = factory.Faker('text')
