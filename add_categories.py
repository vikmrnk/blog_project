import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_app.settings')
django.setup()

from blog.models import Category

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
        print(f"Created category: {category_name}")
    else:
        print(f"Category already exists: {category_name}")

print(f"\nAdded {created_count} new categories to the database.") 