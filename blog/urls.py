from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    CategoryView,
    like_post,
    post_search,
)

urlpatterns = [
    path('', views.signup, name='signup-page'),
    path('login/', views.loginn, name='login-page'),
    path('home/', PostListView.as_view(), name='home-page'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='new-post'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>/posts/', UserPostListView.as_view(), name='user-posts'),
    path('user/<str:username>/profile/', views.profile, name='user-profile'),
    path('profile/update/', views.update_profile, name='update-profile'),
    path('mypost/', views.myPost, name='my-post'),
    path('category/<str:category>/', CategoryView.as_view(), name='category'),
    path('search/', post_search, name='post-search'),
    path('like/<int:pk>/', views.like_post, name='like-post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add-comment'),
    path('comment/<int:comment_id>/reply/', views.add_reply, name='add-reply'),
    path('signout/', views.signout, name='signout-btn'),
    path('add-categories/', views.add_categories, name='add-categories'),
]
