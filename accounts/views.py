from django.shortcuts import render
from django.views.generic import CreateView,TemplateView
from django.urls import reverse_lazy 
from . import forms 

# Create your views here.
class signup(CreateView):
    template_name = "accounts/signup.html"
    form_class = forms.UserForm
    success_url = reverse_lazy('login')

class profileView(TemplateView):
    template_name = "accounts/profile.html"
    

    
    

