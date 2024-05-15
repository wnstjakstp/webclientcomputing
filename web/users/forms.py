from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname','level', 'skill', 'language']
        widgets = {
            'level': forms.RadioSelect,
            'skill': forms.RadioSelect,
            'language': forms.RadioSelect,
        }
