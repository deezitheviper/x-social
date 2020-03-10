from django.shortcuts import render
from django.views.generic import CreateView,TemplateView,UpdateView
from django.urls import reverse_lazy 
from . import forms 
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class signup(CreateView):
    template_name = "accounts/signup.html"
    form_class = forms.UserForm
    success_url = reverse_lazy('login')

class profileView(TemplateView):
    template_name = "accounts/profile.html"
    
class profileUpdate(LoginRequiredMixin,UpdateView):
    template_name = 'accounts/updateprofile.html'
    fields = ['email','password1','password2','avatar']
    form_class = forms.UserForm
    

