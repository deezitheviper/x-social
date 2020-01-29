from django.urls import path,re_path
from . import views
app_name='posts'
urlpatterns = [
    path('',views.PostList.as_view(),name='lists'),
    path('<slug>/create',views.PostCreateView,name='create'),
    path('<username>/',views.UserPosts.as_view(),name='user'),
    path('<username>/<slug>', views.PostDetail.as_view(),name='detail'),
    path('delete/<slug>/',views.PostDeleteView.as_view(),name='delete')
]
