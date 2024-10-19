from django.urls import path
from . import views
from django.contrib.auth.views import LoginView  # Ensure this import is present

urlpatterns = [
path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True), name='login'),
    path('create_post/', views.create_post, name='create_post'),
path('waiting_for_approval/', views.waiting_for_approval, name='waiting_for_approval'),
    path('post_list/', views.post_list, name='post_list'),
path('profile_dashboard/', views.profile_dashboard, name='profile_dashboard'),
    path('approve_user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
path('deny_user/<int:user_id>/', views.deny_user, name='deny_user'),

]