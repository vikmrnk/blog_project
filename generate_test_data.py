import os
import django
import random
from django.utils import timezone
from datetime import timedelta

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_app.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Post, Comment, UserProfile

# Sample data
usernames = ['john_doe', 'jane_smith', 'tech_guru', 'blog_master', 'creative_writer', 
             'story_teller', 'travel_explorer', 'food_lover', 'health_expert', 'finance_pro']

categories = ['Technology', 'Travel', 'Food', 'Health', 'Finance', 
              'Education', 'Sports', 'Entertainment', 'Science', 'Art']

# Avatar colors
avatar_colors = ['#5e60ce', '#5390d9', '#4ea8de', '#48bfe3', '#56cfe1', 
                '#64dfdf', '#72efdd', '#80ffdb', '#ffadad', '#ffc6ff']

# Sample lorem ipsum paragraphs
lorem_paragraphs = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam euismod, nisl eget fermentum aliquam, nisl nunc aliquet nunc, eget aliquam nisl nunc eget nisl. Nullam euismod, nisl eget fermentum aliquam, nisl nunc aliquet nunc, eget aliquam nisl nunc eget nisl.",
    "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet, ante. Donec eu libero sit amet quam egestas semper. Aenean ultricies mi vitae est.",
    "Fusce nec tellus sed augue semper porta. Mauris massa. Vestibulum lacinia arcu eget nulla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Curabitur sodales ligula in libero.",
    "Sed dignissim lacinia nunc. Curabitur tortor. Pellentesque nibh. Aenean quam. In scelerisque sem at dolor. Maecenas mattis. Sed convallis tristique sem. Proin ut ligula vel nunc egestas porttitor.",
    "Morbi lectus risus, iaculis vel, suscipit quis, luctus non, massa. Fusce ac turpis quis ligula lacinia aliquet. Mauris ipsum. Nulla metus metus, ullamcorper vel, tincidunt sed, euismod in, nibh. Quisque volutpat condimentum velit.",
]

post_titles = [
    "The Future of Artificial Intelligence",
    "10 Must-Visit Destinations for 2023",
    "Healthy Recipes for Busy Professionals",
    "Understanding Blockchain Technology",
    "How to Start Investing in Your 20s",
    "Effective Learning Strategies for Students",
    "The Impact of Social Media on Mental Health",
    "Sustainable Travel: Tips for Eco-Friendly Adventures",
    "Building a Personal Brand in the Digital Age",
    "The Science Behind Productivity",
    "Remote Work: Benefits and Challenges",
    "Mindfulness Techniques for Stress Reduction",
    "Cybersecurity Essentials Everyone Should Know",
    "The Art of Storytelling in Marketing",
    "Financial Planning for Young Families",
    "Future Tech Trends to Watch",
    "Healthy Habits for a Balanced Lifestyle",
    "Understanding Climate Change Impact",
    "Leadership Skills for the Modern Workplace",
    "Creative Writing Tips for Beginners"
]

# Clean existing data
print("Cleaning existing data...")
Comment.objects.all().delete()
Post.objects.all().delete()
Category.objects.all().delete()
UserProfile.objects.all().delete()
User.objects.filter(is_superuser=False).delete()

# Create categories
print("Creating categories...")
category_objects = []
for category_name in categories:
    category = Category.objects.create(name=category_name)
    category_objects.append(category)

# Create users
print("Creating users...")
users = []
for username in usernames:
    email = f"{username}@example.com"
    user = User.objects.create_user(username=username, email=email, password="password123")
    
    # Create user profile with random avatar color
    avatar_color = random.choice(avatar_colors)
    profile = UserProfile.objects.create(
        user=user, 
        bio=f"I am {username}. " + random.choice(lorem_paragraphs),
        avatar_color=avatar_color
    )
    
    users.append(user)

# Create posts
print("Creating posts...")
posts = []
for i in range(40):  # Create 40 posts
    author = random.choice(users)
    category = random.choice(category_objects)
    title = random.choice(post_titles) + f" {i+1}"
    
    # Create content from paragraphs
    num_paragraphs = random.randint(3, 6)
    content_paragraphs = random.sample(lorem_paragraphs * 3, num_paragraphs)
    content = "\n\n".join(content_paragraphs)
    
    # Create summary
    summary = content[:150] + "..." if random.choice([True, False]) else ""
    
    # Random date within the last 60 days
    days_ago = random.randint(0, 60)
    date_posted = timezone.now() - timedelta(days=days_ago)
    
    # Random reading time between 2 and 15 minutes
    reading_time = random.randint(2, 15)
    
    post = Post.objects.create(
        title=title,
        content=content,
        summary=summary,
        date_posted=date_posted,
        author=author,
        category=category,
        views=random.randint(5, 500),
        reading_time=reading_time
    )
    
    # Add random likes to the post
    num_likes = random.randint(0, 8)
    likers = random.sample(users, min(num_likes, len(users)))
    for liker in likers:
        post.likes.add(liker)
    
    posts.append(post)

# Create comments
print("Creating comments...")
for post in posts:
    # Generate 0-5 comments per post
    num_comments = random.randint(0, 5)
    for _ in range(num_comments):
        author = random.choice(users)
        content = random.choice(lorem_paragraphs)[:100]
        
        # Random date after post date but before now
        post_date = post.date_posted
        now = timezone.now()
        comment_date = post_date + timedelta(
            seconds=random.randint(0, int((now - post_date).total_seconds()))
        )
        
        comment = Comment.objects.create(
            post=post,
            author=author,
            content=content,
            date_posted=comment_date
        )
        
        # Add 0-3 replies to each comment
        num_replies = random.randint(0, 3)
        for _ in range(num_replies):
            reply_author = random.choice(users)
            reply_content = f"@{author.username} " + random.choice(lorem_paragraphs)[:80]
            
            # Reply date is after comment date but before now
            reply_date = comment_date + timedelta(
                seconds=random.randint(0, int((now - comment_date).total_seconds()))
            )
            
            Comment.objects.create(
                post=post,
                author=reply_author,
                content=reply_content,
                date_posted=reply_date,
                parent=comment
            )

print("Test data generation complete!")
print(f"Created {len(users)} users, {len(category_objects)} categories, {len(posts)} posts, and numerous comments.") 