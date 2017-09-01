"""
Profile Update Views for declined profiles
Author: AmrAnwar
"""
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.views.generic import View, DetailView, FormView
from django.contrib import messages
from django.urls import reverse
from django.views.generic.detail import BaseDetailView

from ..models import Profile


class ProfileView(DetailView):
    context_object_name = "profile"
    template_name = 'profile.html'
    model = Profile

    # def get_initial(self):
    #     """
    #     Returns the initial data to use for the form
    #     """
    #     initial = super(ProfileView, self).get_initial()
    #     initial['first_name'] = self.get_object().user.first_name
    #     initial['last_name'] = self.get_object().user.last_name
    #     return initial
    #
    # def get_form_kwargs(self):
    #     """
    #     add the profile instance data to the form
    #     :return: the ProfileDeclineUpdate Form with the user data
    #     """
    #     form_kwargs = super(ProfileView, self).get_form_kwargs()
    #     form_kwargs['instance'] = self.object()
    #     return form_kwargs
    #
    # # def form_valid(self, form, **kwargs):
    # #     user_data = {
    # #             'first_name': form.cleaned_data.pop('first_name'),
    # #             'last_name': form.cleaned_data.pop('last_name'),
    # #         }
    # #         self.profile.user.__dict__.update(user_data)
    # #         self.profile.user.save()
    # #         form.save()
    # #         details_string = """your profile was updated successfully
    # #         please wait until review it"""
    # #         messages.success(self.request, details_string)
    # #         return HttpResponseRedirect(reverse("account"))

