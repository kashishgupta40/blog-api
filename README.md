# 📝 Blog REST API

This project is a Blog REST API built with Django REST Framework that supports user authentication, blog creation, modification, deletion, liking, commenting, and more.  
It also includes Swagger UI integration for easy API testing.

---

## 🚀 Features

### 1. User Authentication
- Register a new user
- Login with token authentication

### 2. Blog Management
- Create, update, delete blogs
- List blogs with pagination, likes count, and comments count
- View a single blog with latest 5 comments

### 3. Blog Interactions
- Like/Unlike a blog
- Add comments
- List comments with pagination

### 4. API Documentation
- Swagger UI via `drf-yasg` at `/swagger/`
- Redoc at `/redoc/`

---

## 🛠 Tech Stack

- Python
- Django
- Django REST Framework
- drf-yasg


---

## ⚙️ Setup Instructions

### 🔧 Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 📦 Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 🗃 Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 🧪 Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### ▶️ Start the Server

```bash
python manage.py runserver
```

Visit [http://localhost:8000/swagger/](http://localhost:8000/swagger/) for API docs.

---

## 📡 Example API Calls

### Register

```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

### Login

```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepassword"
}
```

### Create Blog

```http
POST /api/blogs/
Authorization: Token <your_token>
Content-Type: application/json

{
  "title": "My First Blog",
  "content": "This is the content of the blog."
}


### Like a Blog

```http
POST /api/blogs/{id}/like/
Authorization: Token <your_token>


### Add Comment

```http
POST /api/blogs/{id}/comments/
Authorization: Token <your_token>
Content-Type: application/json

{
  "content": "Great post!"
}


## 🛡 Permissions

- Only blog authors can update/delete their blogs.
- Authenticated users can like/unlike and comment.
- Unauthenticated users can view blogs and comments.



