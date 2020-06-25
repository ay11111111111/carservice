from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import (CustomUserCreationForm,
                    UserUpdateForm,
                    CustomAuthenticationForm
                    )
from .models import CustomUser
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Your account has been created {email}! You can login now.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form':form})



def logout_view(request):
	logout(request)
	return redirect('home')


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'You are logged in!')
                return redirect("home")
    else:
        form = CustomAuthenticationForm()

    context = {
        'form':form
        }

    return render(request, "users/login.html", context)

#
# @login_required
# def profile(request):
#     if request.method == "POST":
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         # p_form = ProfileUpdateForm(request.POST, instance=request.user)
#         if u_form.is_valid():
#             u_form.save()
#             # p_form.save()
#             messages.success(request, f'Your account has been updated!')
#             return redirect('profile')
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         # p_form = UserUpdateForm(instance=request.user)
#
#     context = {
#         'u_form': u_form,
#         # 'p_form': p_form,
#     }
#     return render(request, 'users/profile.html', context)

#
# @method_decorator(login_required, name='dispatch')
# class ProfileCreateView(CreateView):
#     model = Profile
#     success_url = 'car/create'
#     form_class = ProfileCreationForm
#     def form_valid(self, form):
#         form.instance.user= self.request.user
#         return super().form_valid(form)
