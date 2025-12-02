<h1 align="center">Videoflix</h1>

<p align="center">
  <em>Videoflix is a Django 5.2.8-based backend for a video streaming platform. It supports user registration, authentication with JWT tokens, video upload and streaming, email verification, and password reset. It runs fully in Docker with PostgreSQL and Redis.</em>
  <br>
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.13.2-blue?logo=python&logoColor=white" alt="Python version"></a>
  <a href="https://www.djangoproject.com/"><img src="https://img.shields.io/badge/Django-5.2.8-success?logo=django&logoColor=white" alt="Django version"></a>
  <a href="https://www.django-rest-framework.org/"><img src="https://img.shields.io/badge/DRF-3.16.1-red?logo=django&logoColor=white" alt="DRF version"></a>
</p>

<hr>

## 🔧 Features

- **User authentication & authorization**  
  JWT-based authentication, with tokens stored in HTTP-only cookies for secure web apps.

- **User registration & email verification**  
  Sends activation emails after registration using Django’s email system and background jobs (RQ).

- **Password reset**  
  Secure password reset flow via email with expiring activation tokens.

- **Video management**  
  Upload videos and thumbnails via the admin panel. HLS streaming generation supported.

- **Background tasks**  
  Uses `django-rq` for sending emails asynchronously.

- **Dockerized development & deployment**  
  All services run in Docker: backend, PostgreSQL, Redis.

---

## Prerequisites

- Docker & Docker Compose
- Python 3.13.2 (for local testing outside Docker)
- SMTP email credentials (for sending emails)
- `.env` file with environment variables (see template below)

---

## 📁 Project Structure
```text
videoflix/
├── auth_app/               # Authentication app
├── video_app/              # Video app
├── core/                   # Settings, routing
├── static/                 # Static files (CSS, JS, images)
├── media/                  # Uploaded media files (videos, thumbnails)
├── templates/              # Email and HTML templates
├── backend.Dockerfile      # Dockerfile for backend
├── docker-compose.yml      # Docker Compose config
├── .env.template           # Environment variable template
├── requirements.txt        # Python dependencies
├── backend.entrypoint.sh   # Startup script for Docker container
└── manage.py
```

---

## 📦 Setup

1. **Copy the environment file**
```bash
cp .env.template .env
```

2. **Edit .env**
  Set your database credentials, email server settings, and superuser details.

3. **Build and run Docker containers**
```bash
docker-compose up --build
```

Backend container will automatically:

- Wait for PostgreSQL
- Run migrations
- Create superuser (from .env)
- Start RQ worker for background tasks
- Start Gunicorn server on port 8000

---

## Accessing the backend

API base URL: http://localhost:8000/api/

Django admin: http://localhost:8000/admin/
Use the superuser from .env

---

## Volumes & Media

Docker Compose uses named volumes:

volumes:
  videoflix_media: /app/media
  videoflix_static: /app/static

- Media: User uploads (videos, thumbnails) are stored in /app/media and persisted in videoflix_media.
- Static: Static files and assets (CSS, JS, email logos) are stored in /app/static and persisted in videoflix_static.
- Important: For email logos or other assets referenced in templates, place them in static/images/ inside your project.

---

## JWT Authentication

- Access token: 30 min
- Refresh token: 1 day
- Stored in HTTP-only cookies for security.
- Custom authentication class CookieJWTAuthentication reads tokens from cookies first, then headers.

---

## Sending Emails

Uses Django’s SMTP backend.

Background tasks via django-rq:

- Activation emails
- Password reset emails
- Place your email templates in templates/emails/

Note: During local development, images in emails must use publicly accessible URLs or be attached as inline files (CID).

---

## Running Background Jobs

RQ worker is started automatically by backend.entrypoint.sh.

To manually start a worker:

```bash
docker exec -it videoflix_backend python manage.py rqworker default
```

---

## 🔑 API Endpoints

Authentication
| Method | Endpoint                                 | Description                                    |
| ------ | ---------------------------------------- | ---------------------------------------------- |
| POST   | `/api/registration/`                     | Register a new user and send mail              |
| GET    | `/api/activate/<uidb64>/<token>/`        | Activate account with link from mail           |
| POST   | `/api/login/`                            | Login, sets access & refresh tokens in cookies |
| POST   | `/api/logout/`                           | Logout, deletes cookies                        |
| POST   | `/api/token/refresh/`                    | Refresh the access token                       |
| POST   | `/api/password_reset/`                   | Send mail to reset password                    |
| POST   | `/api/password_confirm/<uidb64>/<token>/`| Accept the password reset                      |


Video
| Method | Endpoint                                                   | Description                 |
| ------ | ---------------------------------------------------------- | --------------------------- |
| GET    | `/api/video/`                                              | Show all videos             |
| GET    | `/api/video/<int:movie_id>/<str:resolution>/index.m3u8`    | Give back HLS file of video |
| GET    | `/api/video/<int:movie_id>/<str:resolution>/<str:segment>/`| Give back HLS video         |

---

## ⚙️ Dependencies

Key Python packages:

Django 5.2.8
djangorestframework 3.16.1
djangorestframework-simplejwt 5.5.1
psycopg2-binary
django-rq
redis
gunicorn
whitenoise

Environment Variables (.env)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=adminpassword
DJANGO_SUPERUSER_EMAIL=admin@example.com

SECRET_KEY="your-secret-key"
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:5500

DB_NAME=videoflix_db
DB_USER=videoflix_user
DB_PASSWORD=supersecretpassword
DB_HOST=db
DB_PORT=5432

REDIS_HOST=redis
REDIS_LOCATION=redis://redis:6379/1
REDIS_PORT=6379
REDIS_DB=0

EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email_user
EMAIL_HOST_PASSWORD=your_email_password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=default_from_email

---

## 📌 Notes

- Videos are uploaded via Django admin and saved in /app/media/videos/.
- Static assets like email logos should be placed in /app/static/images/ for Docker to mount them correctly.
- The project is fully Dockerized for consistent development and deployment.