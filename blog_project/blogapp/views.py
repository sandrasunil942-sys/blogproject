from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import UserRegisterForm, ProfileForm, BlogPostForm, CommentForm
from .models import BlogPost, Comment

# Register
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, ProfileForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # Create user (username is guaranteed present by the form)
            user = user_form.save()

            # Update the auto-created Profile with submitted fields
            profile, _ = Profile.objects.get_or_create(user=user)
            cd = profile_form.cleaned_data
            profile.profile_pic = cd.get('profile_pic')
            profile.contact_number = cd.get('contact_number')
            profile.user_type = cd.get('user_type')
            profile.save()

            login(request, user)  # optional auto-login
            messages.success(request, 'Registration successful!')
            return redirect('home')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()

    return render(request, 'blogapp/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

# Home with Pagination
def home(request):
    posts_list = BlogPost.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 3)  # Show 3 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'blogapp/home.html', {'posts': posts})


# Create Post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Make sure BlogPost has "author" field
            post.save()
            return redirect('home')
    else:
        form = BlogPostForm()
    return render(request, 'blogapp/create_post.html', {'form': form})


# Edit Post
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, author=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blogapp/edit_post.html', {'form': form})


# Delete Post
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blogapp/delete_post.html', {'post': post})


# Post Detail + Comments
def post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'blogapp/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })
