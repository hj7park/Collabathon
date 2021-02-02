from django.urls import path
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    #path('accounts/signup-re/', views.signup_info, name='signup_info'),
    path('posts/', views.post_index, name='post_index'),
    path('posts/<int:cred_id>/', views.post_detail, name='post_detail'),
    path('posts/create/', views.postCreate.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', views.postUpdate.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.postDelete.as_view(), name='post_delete'),
]