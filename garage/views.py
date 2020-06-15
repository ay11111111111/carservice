from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (CarCreationForm)
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from .models import Car
from django.utils.decorators import method_decorator


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
