from django.conf import settings

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View, FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.views.generic import FormView
from django.contrib.auth.models import User

from ..models import Profile
from ..forms import ProfileForm


class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request):
        login_message = "Email/Password Combination is incorrect"
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            messages.error(self.request, login_message)
        return HttpResponseRedirect(reverse('login'))

    def get(self, request):
        if not request.user.is_anonymous():
            return HttpResponseRedirect(reverse('projects-list'))
        return super(LoginView, self).get(request)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = ProfileForm

    def form_valid(self, form):
        """
        If the form is valid, respond with success
        """
        first_name = form.cleaned_data.pop('first_name')
        last_name = form.cleaned_data.pop('last_name')
        email = form.cleaned_data.pop('email')
        username = form.cleaned_data.pop('username')

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username)
        user.save()

        user.set_password(form.cleaned_data.pop('password'))
        user.save()

        form.cleaned_data.update({'user': user})

        profile = Profile(**form.cleaned_data)
        profile.save()

        success_url = 'Registeration Successful'
        messages.success(self.request, success_url)
        return HttpResponseRedirect(reverse("login"))
