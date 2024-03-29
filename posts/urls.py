from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.group_posts, name='group_posts'),
    path('group/', views.group_id, name='group_id'),
    path('search', views.search, name='search'),
    path('new/', views.new_post, name='new_post'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('follow/', views.follow_index, name='follow_index'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path('<str:username>/<int:post_id>/edit/', views.post_edit,
         name='post_edit'),
    path('<str:username>/<int:post_id>/delete/', views.delete_post,
         name='delete_post'),
    path('<str:username>/<int:post_id>/comment', views.add_comment,
         name='add_comment'),
    path('<str:username>/follow/', views.profile_follow,
         name='profile_follow'),
    path('<str:username>/unfollow/', views.profile_unfollow,
         name='profile_unfollow'),
    path('<str:username>/<int:post_id>/like', views.like, name='like'),
]
