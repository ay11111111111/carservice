from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (UserRegisterForm, UserUpdateForm, CarCreationForm,
                    ProfileCreationForm,
                    )
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from .models import Car, Profile
from django.utils.decorators import method_decorator

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can login now.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # p_form = ProfileUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            # p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        # p_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
        # 'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)


@method_decorator(login_required, name='dispatch')
class ProfileCreateView(CreateView):
    model = Profile
    success_url = 'car/create'
    form_class = ProfileCreationForm
    def form_valid(self, form):
        form.instance.user= self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class CarCreateView(CreateView):
    model = Car
    success_url = '/'
    form_class = CarCreationForm
    def form_valid(self, form):
        form.instance.user= self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class CarDetailView(DetailView):
    model = Car
    fields = ['car_model', 'year_of_issue','korobka','probeg']

@method_decorator(login_required, name='dispatch')
class CarUpdateView(UpdateView):
    model = Car
    fields = ['car_model', 'year_of_issue','korobka','probeg']

@method_decorator(login_required, name='dispatch')
class CarDeleteView(DeleteView):
    model = Car
    success_url = '/'
