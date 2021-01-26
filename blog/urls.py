from . import views
from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns=[
    path('',views.signup,name='signup'),
    path('home',views.home,name='home'),
    path('login',LoginView.as_view(), name='login'),
    path('logout',LogoutView.as_view(), name='logout'),
    path('createpost',views.newpost, name='createpost'),
    path('comment/<int:pk>',views.newcomment, name='newcomment'),
    path('posts',views.PostList.as_view(), name='allposts'),
    path('postsbyauthor/<int:pk>',views.PostListbyAuthor.as_view(), name='postsbyauthor'),
    path('post/<int:pk>',views.PostDetail.as_view(), name='postdetail'),
]