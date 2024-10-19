from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import CustomUser, Post, Report, UserPreference
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account successfully created. Awaiting admin approval.")
            return redirect('profile_dashboard')  # Redirect to waiting page
        else:
            messages.error(request, "There was an error creating your account. Please try again.")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})



from django.shortcuts import render

def waiting_for_approval(request):
    return render(request, 'waiting_for_approval.html')


def profile_dashboard(request):
    return render(request, 'profile_dashboard.html', {'user': request.user})

def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if not Post.objects.filter(user=request.user).exists():
            Post.objects.create(user=request.user, content=content)
            messages.success(request, "Post created successfully.")
            return redirect('post_list')
        else:
            messages.error(request, "You can only create one post.")
            return redirect('create_post')

    return render(request, 'create_post.html')

from django.core.paginator import Paginator
from django.utils.html import format_html

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'post_list.html', {'page_obj': page_obj})

def truncate_content(content, length=100):
    if len(content) > length:
        return format_html('{}... <a href="#" class="see-more">see more</a>', content[:length])
    return content

from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator


def admin_dashboard(request):
    # Users pending approval
    pending_users = CustomUser.objects.filter(is_active=False).order_by('-date_joined')
    user_paginator = Paginator(pending_users, 5)
    user_page = request.GET.get('user_page')
    user_page_obj = user_paginator.get_page(user_page)

    # Posts management
    posts = Post.objects.all().order_by('-created_at')
    post_paginator = Paginator(posts, 5)
    post_page = request.GET.get('post_page')
    post_page_obj = post_paginator.get_page(post_page)

    # Reports
    reports = Report.objects.all().order_by('-created_at')
    report_paginator = Paginator(reports, 5)
    report_page = request.GET.get('report_page')
    report_page_obj = report_paginator.get_page(report_page)

    return render(request, 'admin_dashboard.html', {
        'user_page_obj': user_page_obj,
        'post_page_obj': post_page_obj,
        'report_page_obj': report_page_obj
    })
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages


def approve_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f"User {user.username} has been approved.")
    return redirect('admin_dashboard')


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, "Post has been deleted.")
    return redirect('admin_dashboard')


def deny_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()  # Delete the user from the database
    messages.success(request, f"User {user.username} has been denied and removed.")
    return redirect('admin_dashboard')
