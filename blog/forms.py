from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Post, Comment, Category

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']
        
class ProfileUpdateForm(forms.ModelForm):
    avatar_color = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
        help_text="Choose your avatar background color"
    )
    
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar_color']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5}),
        }

class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        required=False,
        empty_label="Select a category (optional)"
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'summary', 'category', 'reading_time']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Content', 'rows': 10}),
            'summary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Summary (optional)'}),
            'reading_time': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '60', 'value': '3'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Write your comment here...', 
                'rows': 3
            }),
        }
        labels = {
            'content': '',
        } 