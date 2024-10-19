from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashdash, name='admin_dashdash'),
    path('approve_user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
]
