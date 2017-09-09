from django import forms
from ..models import Profile
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()

    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'about',
            'image',
        )

    def clean_email(self):
        """
        check if email already exists
        :return: email if it's not exists else raise ValidationError
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Email already exists')
        return email
