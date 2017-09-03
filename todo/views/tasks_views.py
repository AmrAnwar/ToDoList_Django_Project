from django.views.generic import DetailView, UpdateView
from ..models import Task
from django.http import Http404


class TaskDetailView(UpdateView, DetailView):
    context_object_name = "task"
    fields = ['title', 'file', 'description', 'status', 'points']
    template_name = 'task.html'
    model = Task

    def dispatch(self, request, *args, **kwargs):
        if request.user not in self.get_object().list.users.all():
            raise Http404
        return super(TaskDetailView, self).dispatch(request, *args, **kwargs)
