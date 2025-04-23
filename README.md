# BlogBridges

BlogBridges is a powerful blog platform built with Django that allows users to create, view, and interact with content through an intuitive user interface.


## Features

- **User System**: Registration, login, profiles with avatars and biographies
- **Content Creation and Editing**: Content editor for posts
- **Post Categories**: Organization of articles by categories
- **Likes and Comments**: Interaction with posts
- **Comment Replies**: Ability to reply to comments
- **Search**: Quick search by titles, content, and authors
- **Category Filtering**: View articles by specific category
- **View Tracking**: View counter for each post
- **Responsive Design**: User-friendly on all devices
- **Protected Routes**: Access to features only for authorized users

## Technologies

- **Backend**: Django 5.1
- **Frontend**: Bootstrap 4, jQuery, Font Awesome
- **Database**: SQLite (easily replaceable with PostgreSQL for production)
- **Media Storage**: Local media file storage

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtualenv (optional but recommended)

## Installation

1. **Clone the repository**:
   ```bash
   git clone
   cd Blog-Bridges
   ```

2. **Create a virtual environment** (optional):
   ```bash
   python -m venv venv
   source venv/bin/activate  # for Linux/Mac
   # or
   venv\Scripts\activate  # for Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create migrations and apply them to the database**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser** (for admin panel access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the site** through a browser at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Usage

### Registration and Login

- Visit the homepage to register
- Log in using your credentials

### Creating Content

1. Click on "New Post" in the navigation bar
2. Add title, content, and optionally a category and image
3. Click "Publish Post"

### Search and Filtering

- Use the search bar at the top to search for posts
- Use the sidebar categories to filter by topic

### Commenting and Interaction

- Click on a post to read the full content
- Leave comments at the bottom of the page
- Click "Reply" to respond to a specific comment
- Click the heart icon to like a post

### User Profile

- Visit your profile to see all your posts
- Update your profile by adding a photo and biography

### Administration (for superusers)

- Access the admin panel at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
- Manage all users, posts, comments, and categories

## Project Structure

```
Blog-Bridges/
├── blog/                   # Main blog application
│   ├── migrations/         # Database migrations
│   ├── static/             # Static files (CSS, JS, images)
│   ├── templates/          # HTML templates
│   ├── admin.py            # Admin panel settings
│   ├── forms.py            # Application forms
│   ├── models.py           # Data models
│   ├── urls.py             # URL routes
│   └── views.py            # View logic
├── blog_app/               # Project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL routes
│   └── wsgi.py             # WSGI configuration
├── media/                  # Uploaded media files
├── manage.py               # Django management script
├── requirements.txt        # Project dependencies
└── README.md               # Documentation
```

## Author

Viktoriia Kamarenko - [https://github.com/vikmrnk](https://github.com/vikmrnk)