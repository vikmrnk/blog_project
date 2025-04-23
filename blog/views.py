from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from blog import models
from .models import Post, Category, Comment, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.db.models import Q, Count
from .forms import UserUpdateForm, ProfileUpdateForm, PostForm, CommentForm
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('uname')
        email= request.POST.get('uemail')
        password = request.POST.get('upassword')
        
        # Check if username already exists
        if User.objects.filter(username=name).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return render(request, 'blog/signup.html')
            
        newUser = User.objects.create_user(username=name, email=email, password=password)
        newUser.save()
        
        # Create user profile
        UserProfile.objects.create(user=newUser)
        
        messages.success(request, f'Account created for {name}! You can now log in.')
        return redirect('/login')
    return render(request, 'blog/signup.html')


def loginn(request):
    if request.method == 'POST':
        name = request.POST.get('uname')
        password = request.POST.get('upassword')
        userr = authenticate(request, username=name, password=password)
        if userr is not None:
            login(request, userr)
            next_page = request.GET.get('next')
            return redirect(next_page) if next_page else redirect('/home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('/login')

    return render(request, 'blog/login.html')


def add_categories(request):
    # List of categories to add
    categories = [
        'Technology',
        'Travel',
        'Food',
        'Health',
        'Finance',
        'Education',
        'Sports',
        'Entertainment',
        'Science',
        'Art'
    ]
    
    # Create categories
    created_count = 0
    for category_name in categories:
        category, created = Category.objects.get_or_create(name=category_name)
        if created:
            created_count += 1
    
    messages.success(request, f'Added {created_count} new categories to the database.')
    return redirect('home-page')


@login_required
def home(request):
    context = {
        'posts': Post.objects.all().order_by('-date_posted'),
        'categories': Category.objects.all(),
        'featured_authors': User.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:5]
    }
    return render(request, 'blog/home.html', context)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['users_count'] = User.objects.count()
        context['featured_authors'] = User.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:5]
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Increase view count
        post.increase_views()
        
        # Check if user has liked post
        if self.request.user.is_authenticated:
            context['liked'] = post.likes.filter(id=self.request.user.id).exists()
        
        # Add comment form
        context['comment_form'] = CommentForm()
        context['comments'] = post.comments.filter(parent=None).order_by('-date_posted')
        
        # Add categories and recent posts
        context['categories'] = Category.objects.all()
        context['recent_posts'] = Post.objects.exclude(id=post.id).order_by('-date_posted')[:5]
        
        # Add related posts by category if available
        if post.category:
            context['related_posts'] = Post.objects.filter(category=post.category).exclude(id=post.id).order_by('-date_posted')[:3]
        
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated!')
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('home-page')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your post has been deleted!')
        return super().delete(request, *args, **kwargs)


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, username=self.kwargs.get('username'))
        return context


class CategoryView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        category = get_object_or_404(Category, name=self.kwargs.get('category'))
        return Post.objects.filter(category=category).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category')
        context['categories'] = Category.objects.all()
        return context


@login_required
def post_search(request):
    query = request.GET.get('q')
    
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        ).distinct().order_by('-date_posted')
        
        paginator = Paginator(results, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'blog/search_results.html', {
            'page_obj': page_obj,
            'query': query,
            'count': results.count(),
            'categories': Category.objects.all()
        })
    
    return redirect('home-page')


@login_required
def like_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=pk)
        
        # Check if the user already liked the post
        if post.likes.filter(id=request.user.id).exists():
            # User already liked the post, so unlike it
            post.likes.remove(request.user)
            liked = False
        else:
            # User hasn't liked the post, so like it
            post.likes.add(request.user)
            liked = True
        
        # Return JSON response with the updated like status and count
        return JsonResponse({
            'liked': liked,
            'like_count': post.likes.count()
        })
    
    # If not a POST request, redirect to post detail
    return redirect('post-detail', pk=pk)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('post-detail', pk=post.id)
    
    return redirect('post-detail', pk=post.id)


@login_required
def add_reply(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = parent_comment.post
            reply.author = request.user
            reply.parent = parent_comment
            reply.save()
            messages.success(request, 'Your reply has been added!')
    
    return redirect('post-detail', pk=parent_comment.post.id)


@login_required
def myPost(request):
    context = {
        'posts': Post.objects.filter(author=request.user).order_by('-date_posted'),
        'categories': Category.objects.all()
    }
    return render(request, 'blog/mypost.html', context)


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-date_posted')
    
    # Get counts for likes and comments
    liked_count = Post.objects.filter(likes=user).count()
    comment_count = Comment.objects.filter(author=user).count()
    
    context = {
        'user_profile': user,
        'profile': UserProfile.objects.get_or_create(user=user)[0],
        'posts': posts,
        'post_count': posts.count(),
        'liked_count': liked_count,
        'comment_count': comment_count,
        'categories': Category.objects.all()
    }
    return render(request, 'blog/profile.html', context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.userprofile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('user-profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'blog/update_profile.html', context)


@login_required
def signout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('/login')

