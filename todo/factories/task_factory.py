import factory
from ..models import List, Task


class TaskFactory(factory.DjangoModelFactory):
    class Meta:
        model = Task
    title = factory.sequence(lambda n: "task %s" % n)
    list = factory.Iterator(List.objects.all())
    user = factory.LazyAttribute(lambda obj: obj.list.project.users.all().first())
    points = factory.Iterator([1, 2, 3, 4])
    description = factory.Faker('text')
    file = factory.django.FileField()
    status = factory.Iterator([1, 2, 3, 4])
