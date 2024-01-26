from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from facebook.models import Profile
from user.forms import RegisterForm, UpdateProfileForm
from user.models import CustomUser


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'register.html', context)


    def post(self, request):
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            register_form.save()
            username = request.POST.get('username')
            user = CustomUser.objects.get(username=username)
            Profile.objects.create(user=user)
            return redirect('login')
        else:
            context = {
                'register_form': register_form
            }
            return render(request, 'register.html', context)





class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'login.html', context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('home')
        else:
            context = {
                'login_form': login_form
            }
            return render(request, 'login.html', context)





class LogoutView(View):
    pass





class UpdateProfileView(View):
    def get(self, request):
        user = request.user
        update_form = UpdateProfileForm(instance=user)
        context = {
            'update_form': update_form,
        }
        return render(request, 'update-profile.html', context)


    def post(self, request):
        user = request.user
        update_form = UpdateProfileForm(instance=user,
                                        data=request.POST,
                                        files=request.FILES)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, 'You have successfully updated your profile data')

            return redirect('user-profile')
        else:
            context = {
                'update_form': update_form,
            }
            return render(request, 'update-profile.html', context)














