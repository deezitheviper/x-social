from django.urls import path
from . import views
app_name='posts'
urlpatterns = [
    path('',views.PostList.as_view(),name='lists'),
    path('create/',views.PostCreateView.as_view(),name='create'),
    path('<username>/',views.UserPosts.as_view(),name='for_user'),
    path('<username>/<slug>', views.PostDetail.as_view(),name='detail'),
    path('delete/<slug>/',views.PostDeleteView.as_view(),name='delete')
]
