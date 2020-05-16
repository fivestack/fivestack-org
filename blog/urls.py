from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/new/', views.post_new, name='post_new'),
    path('posts/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('drafts/', views.draft_list, name='post_draft_list'),
    path('posts/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('posts/<int:pk>/unpublish/', views.post_unpublish, name='post_unpublish'),
    path('posts/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comments/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comments/<int:pk>/remove/', views.comment_delete, name='comment_delete'),
]
