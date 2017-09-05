from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import get_object_or_404

from ..models import List, Code
from ..forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class ListDetailView(LoginRequiredMixin, UpdateView, DetailView):
    model = List
    context_object_name = 'list'
    template_name = 'list_detail.html'
    fields = ['title', 'description', 'users', 'image']

    def form_valid(self, form):
        messages.success(self.request, "List Updated")
        return super(ListDetailView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.task_form = TaskForm(request.POST, prefix="task_form")
        self.object = self.get_object()
        if self.request.user in self.object.users.all():
            return super(ListDetailView, self).dispatch(request, *args, **kwargs)
        raise Http404

    def get_context_data(self, **kwargs):
        kwargs['task_form'] = self.task_form
        return super(ListDetailView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        if request.POST.get("prof1"):
            for email in request.POST:
                if "prof" in email.__str__():
                    user = get_object_or_404(User, email=request.POST.get(email))
                    code = Code.objects.create(user=user, list=self.get_object())
                    print code.code, code.list
                    messages.success(request, "Members added")
        task_form = TaskForm(request.POST, prefix="task_form")
        if task_form.is_valid():
            instance = task_form.save(commit=False)
            instance.user = self.request.user
            instance.list = self.object
            instance.save()
            messages.success(request, "Task Added")
        return super(ListDetailView, self).post(self, request)


@login_required
def list_invite(request, pk=None, code=None):
    code_guest = get_object_or_404(Code, code=code)
    if code_guest.user not in code_guest.list.users.all():
        messages.success(request, "you added to the list")
    else:
        messages.warning(request, "You are already in the list")
    code_guest.list.users.add(code_guest.user)
    return HttpResponseRedirect(reverse("lists-detail",
                                        kwargs={"pk": code_guest.list.pk}))


class ListsView(LoginRequiredMixin, CreateView, ListView):
    context_object_name = 'lists'
    model = List
    template_name = 'list_list.html'
    fields = ['title', 'description', 'image', 'users']

    def form_valid(self, form):
        """
        add the owner user to the form
        :param form: the new form object
        :return:
        """
        form.instance.user = self.request.user
        form.instance = form.save()
        form.instance.users.add(self.request.user)
        return super(ListsView, self).form_valid(form)

    def get_queryset(self):
        """
        :return: filter forms by form owner user
        """
        return self.model.objects.filter(users__id=self.request.user.id)

    def get_context_data(self, **kwargs):
        return super(ListsView, self).get_context_data(**kwargs)
