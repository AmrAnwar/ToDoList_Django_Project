"""
Profile Update Views for declined profiles
Author: AmrAnwar
"""
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.views.generic import View, DetailView, FormView, UpdateView
from django.contrib import messages
from django.urls import reverse
from django.views.generic.detail import BaseDetailView

from ..models import Profile
from django.contrib.auth.models import User
from ..forms import ProfileFormUpdate


class ProfileView(FormView):
    form_class = ProfileFormUpdate
    template_name = 'profile.html'

    def dispatch(self, request, *args, **kwargs):
        """
        check if user is exist else raise 404
        :param request:
        :param args:
        :param kwargs:
        """
        self.user = get_object_or_404(User, username=kwargs['username'])
        self.profile = self.user.profile
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        add the profile instance to the context data
        :param kwargs:
        :return:
        """
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['profile'] = self.profile
        return context

    def get_initial(self):
        """
        add the User object data to the initial data
        """
        initial = super(ProfileView, self).get_initial()
        initial['first_name'] = self.user.first_name
        initial['last_name'] = self.user.last_name
        return initial

    def get_form_kwargs(self):
        """
        add the profile instance data to the form
        :return: the ProfileDeclineUpdate Form with the user data
        """
        form_kwargs = super(ProfileView, self).get_form_kwargs()
        form_kwargs['instance'] = self.profile
        return form_kwargs

    def form_valid(self, form, **kwargs):
        """
        // if form is valid pop['first_name', 'last_name'] from the form then
            add them to the User object data
        // save the form object then create success message
        :param form:
        :param kwargs:
        :return: redirect to profile detail
        """
        user_data = {
                'first_name': form.cleaned_data.pop('first_name'),
                'last_name': form.cleaned_data.pop('last_name'),
        }
        self.profile.user.__dict__.update(user_data)
        self.profile.user.save()
        form.save()
        details_string = """your profile was updated successfully
        please wait until review it"""
        messages.success(self.request, details_string)
        return HttpResponseRedirect(reverse("profile-detail",
                                            kwargs={'username': self.user.username}))
