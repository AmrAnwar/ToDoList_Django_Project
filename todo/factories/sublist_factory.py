import factory
from ..models import List, Task, Sublist


class SubListFactory(factory.DjangoModelFactory):
    class Meta:
        model = Sublist

    title = factory.sequence(lambda n: "sublist %s" % n)
    task = factory.Iterator(Task.objects.all())

