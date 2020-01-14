from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .models import Post
from . import forms
from django.http import Http404
from braces.views import SelectRelatedMixin
from django.views.generic import CreateView,ListView,DetailView,DeleteView

User = get_user_model()

# Create your views here.
class PostList(SelectRelatedMixin,ListView):
    model = Post
    select_related = ('user','group')
    template_name = 'posts/post_list.html'




class PostCreateView(CreateView,LoginRequiredMixin,SelectRelatedMixin):
    model = Post
    template_name = "posts/post_form.html"
    fields = ('name','content')

    def form_valid(self):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)




class UserPosts(ListView):
    model = Post
    template_name='posts/post_list.html'

    def get_queryset(self):
        try:
            self.post.user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post.user 
        return context




class PostDetail(DetailView,SelectRelatedMixin):
    model = Post
    template_name='posts/post_details.html'  

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))




class PostDeleteView(DeleteView,LoginRequiredMixin,SelectRelatedMixin):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user_id)

    def delete(self,*args,**kwargs):
        message.success(self.request,'Post Deleted Successfully')
        return super().delete(*args, **kwargs)    

    
    #09054986096

    


        
        
    


