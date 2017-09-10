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

from ..models import List, Code, Project
from ..forms import ListForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class ProjectDetailView(LoginRequiredMixin, UpdateView, DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'project_detail.html'
    fields = ['title', 'description', 'users']

    def form_valid(self, form):
        """
        if form is valid create success message
        :param form:
        """
        messages.success(self.request, "Project Updated")
        return super(ProjectDetailView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        """
        create form object from(TaskForm) and create prefix for it ("list_form")
        check if user in the project before GET or POST request if not << raise 404
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.list_form = ListForm(request.POST, prefix="list_form")
        self.object = self.get_object()
        if self.request.user in self.object.users.all():
            return super(ProjectDetailView, self).dispatch(request, *args, **kwargs)
        raise Http404

    def get_context_data(self, **kwargs):
        """
        add the object form(task_form) to the context_data
        :param kwargs:
        """
        kwargs['list_form'] = self.list_form
        return super(ProjectDetailView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """
        // Post method to check if list form is valid << create new task with success message
        // and check if there are post("prof1") request to add new  members to the project
            if POST request ("prof1") then will make for..loop-
            into the query to get all the users emails
        :param request:
        :param args:
        :param kwargs:
        """
        if request.POST.get("prof1"):
            for email in request.POST:
                if "prof" in email.__str__():
                    user = get_object_or_404(User, email=request.POST.get(email))
                    code = Code.objects.create(user=user, project=self.get_object())
                    print code.code, code.project
                    messages.success(request, "the members invitations were sent")
        list_form = ListForm(request.POST, prefix="list_form")
        if list_form.is_valid():
            instance = list_form.save(commit=False)
            instance.user = self.request.user
            instance.project = self.object
            instance.save()
            messages.success(request, "List Added")
        return super(ProjectDetailView, self).post(self, request)


@login_required
def project_invite(request, code=None):
    """
    get the invitation code then add the code.user to the code.project
    then << redirect to code.project detail page
    :param request:
    :param code: Project detail url
    :return:
    """
    code_guest = get_object_or_404(Code, code=code)
    if code_guest.user not in code_guest.project.users.all():
        messages.success(request, "you added to the Project")
    else:
        messages.warning(request, "You are already in the Project")
    code_guest.project.users.add(code_guest.user)
    return HttpResponseRedirect(reverse("projects-detail",
                                        kwargs={"pk": code_guest.project.pk}))


class ProjectListView(LoginRequiredMixin, CreateView, ListView):
    context_object_name = 'projects'
    model = Project
    template_name = 'project_list.html'
    fields = ['title', 'description']

    def form_valid(self, form):
        """
        add the owner user to the form
        :param form: the new form object
        """
        form.instance.user = self.request.user
        form.instance = form.save()
        form.instance.users.add(self.request.user)
        return super(ProjectListView, self).form_valid(form)

    def get_queryset(self):
        """
        :return: filter forms by form owner user
        """
        print self.model.objects.all()
        return self.model.objects.filter(users__id=self.request.user.id)
