from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
)
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.forms import formset_factory, modelformset_factory

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect

from ..models import List
from ..forms import TaskForm


class ListDetailView(LoginRequiredMixin, UpdateView, DetailView):
    model = List
    context_object_name = 'list'
    template_name = 'list_detail.html'
    fields = ['title', 'description', 'users', 'image']

    def dispatch(self, request, *args, **kwargs):
        self.form = TaskForm(request.POST or None)
        self.object = self.get_object()
        if self.request.user in self.object.users.all():
            return super(ListDetailView, self).dispatch(request, *args, **kwargs)
        raise Http404

    def get_context_data(self, **kwargs):
        kwargs['task_form'] = self.form
        return super(ListDetailView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            instance = self.form.save(commit=False)
            instance.user = self.request.user
            instance.list = self.object
            instance.save()
            messages.success(request, "Task Added")
            return HttpResponseRedirect(reverse("lists-detail", kwargs={'pk': self.object.pk}))
        else:
            messages.error(request, "form isn't valid")
            return HttpResponseRedirect(reverse("lists-detail", kwargs={'pk': self.object.pk}))


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