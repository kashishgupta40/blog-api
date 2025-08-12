This project is a Blog REST API built with Django REST Framework that supports user authentication, blog creation, modification, deletion, liking, commenting, and more.  
It also includes Swagger UI integration for easy API testing.


## 🚀 Features

1. User Authentication
   - Register a new user
   - Login with token authentication

2. Blog Management
   - Create a new blog
   - Modify an existing blog
   - Delete a blog
   - List all blogs with pagination, likes count, and comments count
   - View a single blog with latest 5 comments, likes count, and comments count

3. Blog Interactions
   - Like/Unlike a blog (only if previously liked)
   - Comment on a blog
   - List all comments for a blog (with pagination)

4. API Documentation
   - Integrated Swagger UI using `drf-yasg` for testing APIs


🛠 Tech Stack

- Python
- Django 
- Django REST Framework 
- Django YASG

