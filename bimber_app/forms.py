from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'age', 'gender', 'city', 'bio', 'photo')

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age > 60 or age <= 16:
            raise forms.ValidationError("Age must be from 16 to 60 years")
        return age



class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'age', 'gender', 'city', 'bio', 'photo')
