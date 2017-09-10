from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
)
from django.http import Http404

from ..models import List
from ..forms import TaskForm


class ListDetailView(LoginRequiredMixin, UpdateView, DetailView):
    model = List
    context_object_name = 'list'
    template_name = 'list_detail.html'
    fields = ['title', 'description', 'image']

    def form_valid(self, form):
        """
        if form is valid create success message
        :param form:
        """
        messages.success(self.request, "List Updated")
        return super(ListDetailView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """
        create form object from(TaskForm) and create prefix for it ("task_form")
        check if user in the list before GET or POST request if not << raise 404
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.task_form = TaskForm(request.POST, prefix="task_form")
        self.object = self.get_object()
        if self.request.user in self.object.project.users.all():
            return super(ListDetailView, self).dispatch(request, *args, **kwargs)
        raise Http404

    def get_context_data(self, **kwargs):
        """
        add the object form(task_form) to the context_data
        :param kwargs:
        """
        kwargs['task_form'] = self.task_form
        return super(ListDetailView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        // Post method to check if task form is valid << create new task with success message
        // and check if there are post("prof1") request to add new  members to the list
            if POST request ("prof1") then will make for..loop-
            into the query to get all the users emails
        :param request:
        :param args:
        :param kwargs:
        """
        task_form = TaskForm(request.POST, prefix="task_form")
        if task_form.is_valid():
            instance = task_form.save(commit=False)
            instance.user = self.request.user
            instance.list = self.object
            instance.save()
            messages.success(request, "Task Added")
        return super(ListDetailView, self).post(self, request)


class ListsView(LoginRequiredMixin, ListView):
    context_object_name = 'lists'
    model = List
    template_name = 'list_list.html'

    def get_queryset(self):
        """
        :return: filter lists by form projects.users
        """
        qs_id = [list.id for list in self.model.objects.all()
               if self.request.user in list.project.users.all()]
        return self.model.objects.filter(id__in=qs_id)
