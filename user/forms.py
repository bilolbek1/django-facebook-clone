from django.contrib.auth.models import User
from django.forms import ModelForm

from user.models import CustomUser


class RegisterForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()

        return user



class UpdateProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'image', 'email', 'first_name', 'last_name']


























