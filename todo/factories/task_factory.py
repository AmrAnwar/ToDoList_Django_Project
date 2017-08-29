import factory
from ..models import List, Task


class TaskFactory(factory.DjangoModelFactory):
    class Meta:
        model = Task
    title = factory.sequence(lambda n: "task %s" % n)
    list = factory.Iterator(List.objects.all())
    user = factory.LazyAttribute(lambda obj: obj.list.users.all().first())



