from django import forms
from ..models import Sublist


class SubListForm(forms.ModelForm):
    class Meta:
        model = Sublist
        fields = [
            'title',
        ]
