from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.paginator import Paginator
from posts.models import Post
from .forms import UserForm, ProfileForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatyczne zalogowanie po rejestracji
            return redirect('profile')  # Przekierowanie do profilu
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    
    paginator = Paginator(user_posts, 5)  # 5 postów na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    post_count = user_posts.count()
    
    context = {
        'profile_user': profile_user,
        'page_obj': page_obj,
        'post_count': post_count,
    }
    
    return render(request, 'accounts/user_profile.html', context)

@login_required
def profile(request):
    user = request.user
    user_posts = Post.objects.filter(author=user).order_by('-created_at')
    post_count = user_posts.count()
    paginator = Paginator(user_posts, 5)  # 5 postów na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'accounts/profile.html', {'user': user,'post_count': post_count, 'page_obj': page_obj})



@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Twój profil został zaktualizowany.')
            return redirect('profile')
        else:
            messages.error(request, 'Wystąpił błąd podczas zapisywania profilu. Spróbuj ponownie.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })