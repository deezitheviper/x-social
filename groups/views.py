from django.shortcuts import render,get_object_or_404
from django.views.generic import CreateView,ListView,DetailView,RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from groups.models import Group,GroupMember
from django.urls import reverse_lazy,reverse
from django.contrib import messages 
from django.db import IntegrityError
from posts.forms import  PostForm

# Create your views here.
class NewGroup(CreateView,LoginRequiredMixin,PermissionRequiredMixin):
    model = Group
    fields = ('name','description')
    template_name = 'groups/group_form.html'

class GroupList(ListView):
    model = Group
    template_name = 'groups/group_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_user = self.request.user.group_set.all()
        context["user_group"] = group_user
        return context
        
class GroupDetail(DetailView):
    model = Group
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm
        return context
    

class JoinGroup(LoginRequiredMixin,RedirectView):
    model = Group

    def get_redirect_url(self,*args, **kwargs):
        return reverse('groups:detail',kwargs={'slug':self.kwargs.get('slug')})
    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except  IntegrityError:
            messages.warning(self.request, 'Already a member')
        else:
            messages.success(self.request,'Joined')
        return super().get(request,*args, **kwargs)

class LeaveGroup(LoginRequiredMixin,RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:detail',kwargs={'slug':self.kwargs.get('slug')})

    def get(self, *args, **kwargs):
        try:
            membership = GroupMember.objects.filter(user=self.request.user,group__slug=self.kwargs.get('slug')).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request,'You are not in this Community')
        else:
            membership.delete()
            messages.success(self.request, 'You have left the Community')   
        return super().get(self.request,*args, **kwargs)             


    

