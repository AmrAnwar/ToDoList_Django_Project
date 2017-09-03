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
from ..forms import ProfileForm


class ProfileView(FormView):
    form_class = ProfileForm
    # context_object_name = "profile"
    template_name = 'profile.html'
    # model = Profile
    # fields = ['following', 'about', 'image']

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(User, username=kwargs['username'])
        self.profile = self.user.profile
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['profile'] = self.profile
        return context

    def get_initial(self):
        """
        Returns the initial data to use for the form
        """
        initial = super(ProfileView, self).get_initial()
        initial['first_name'] = self.user.first_name
        initial['last_name'] = self.user.last_name
        initial['email'] = self.user.email
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


