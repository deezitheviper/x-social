from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .models import Post
from groups.models import Group
from . import forms
from django.http import Http404
from braces.views import SelectRelatedMixin
from django.views.generic import CreateView,ListView,DetailView,DeleteView
from django.contrib.auth.decorators import login_required

User = get_user_model()

# Create your views here.
class PostList(SelectRelatedMixin,ListView):
    model = Post
    select_related = ('user','group')
    template_name = 'posts/post_list.html'



@login_required
def PostCreateView(request,slug):
    group = get_object_or_404(Group,slug=slug)
    template_name = "posts/post_form.html"
    if request.method == 'POST':
        form = forms.PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.group = group
            print('group')
            post.user = request.user
            print(post.user)
            print(post)
            post.save()
            return redirect('groups:detail',slug=slug)
    else:
        form = forms.PostForm()
    return render(request,'posts/post_form.html',{'form':form})        





class UserPosts(ListView):
    model = Post
    template_name='posts/user_post_list.html'

    def get_queryset(self):
        
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
            print('pass')
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context




class PostDetail(DetailView,SelectRelatedMixin):
    model = Post
    template_name='posts/post_details.html'  
    select_related = ("user", "group")


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))




class PostDeleteView(LoginRequiredMixin,DeleteView,SelectRelatedMixin):
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user_id)

    def delete(self,*args,**kwargs):
        message.success(self.request,'Post Deleted Successfully')
        return super().delete(*args, **kwargs)    

    

    


        
        
    


