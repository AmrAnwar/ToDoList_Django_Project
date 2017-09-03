from django import forms
from ..models import Profile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'email',
            'about',
            'image',
        )
