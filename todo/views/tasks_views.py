from django.views.generic import DetailView, UpdateView
from django.http import Http404
from django.contrib import messages

from ..forms import SubListForm
from ..models import Task


class TaskDetailView(UpdateView, DetailView):
    context_object_name = "task"
    fields = ['title', 'file', 'description', 'status', 'points']
    template_name = 'task.html'
    model = Task

    def dispatch(self, request, *args, **kwargs):
        """
        check if user in the task list esle << raise 404
        :param request:
        :param args:
        :param kwargs:
        """
        self.sublist_form = SubListForm(request.POST, prefix="sublist_form")
        if request.user not in self.get_object().list.project.users.all():
            raise Http404
        return super(TaskDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        add the sublist form object to the context data
        :param kwargs:
        """
        kwargs['sublist_form'] = self.sublist_form
        return super(TaskDetailView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        """
        if the update task form is valid create success message
        :param form:
        """
        messages.success(self.request, "Task Updated")
        return super(TaskDetailView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        check if SublistForm is valid << create new sublist in this task detail
        :param request:
        :param args:
        :param kwargs:
        """
        sublist_form = SubListForm(request.POST, prefix="sublist_form")
        if sublist_form.is_valid():
            instance = sublist_form.save(commit=False)
            instance.user = self.request.user
            instance.task = self.get_object()
            instance.save()
            messages.success(request, "SubList Added")
        return super(TaskDetailView, self).post(self, request)
