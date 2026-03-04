from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'age', 'gender', 'city', 'bio', 'photo')

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age > 60 or age < 16:
            raise forms.ValidationError("Age must be from 16 to 60 years")
        return age


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'photo', 'age', 'gender', 'city', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female')]),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')

        if age is None:
            return None

        if age > 60 or age < 16:
            raise forms.ValidationError("Age must be from 16 to 60 years")
        return age
