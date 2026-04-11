# FitBrigade 3.0

A Django web application for planning and tracking workout routines, built as part of the UCD Professional Academy Full Stack Developer Diploma.

**Live Application:** https://fitbrigade-django.onrender.com

## Overview

FitBrigade allows users to create and manage personalised workout sessions, set fitness goals, track progress through statistics, and communicate with other users via an inbox system.

## Features

- **User Authentication** — Register, login, logout, password reset via email
- **Profile Management** — Update personal details and profile picture
- **Workout Tracking** — Create, edit, delete workouts with muscle groups and exercises
- **Goals System** — Set fitness goals, mark them as complete, track progress
- **Statistics** — View workout frequency by muscle group and goal completion rate
- **Messaging Inbox** — Send, receive, and archive messages between users
- **Responsive Design** — Bootstrap 5, mobile-friendly layout

## Tech Stack

- **Backend:** Django 5.0.6 (Python)
- **Database:** PostgreSQL (production) / SQLite (local development)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication:** Django built-in auth + CustomUser model
- **Image Handling:** Pillow (profile picture resize)
- **Deployment:** Render.com + Whitenoise

## Database Design

FitBrigade uses PostgreSQL with Django ORM. The schema follows Third Normal Form (3NF) with two bridge tables to handle many-to-many relationships:

**WorkoutMuscleGroup** — Links Workouts to MuscleGroups. A workout can target multiple muscle groups (e.g., Leg Day → Quadriceps + Glutes + Hamstrings).

**WorkoutExercise** — Links Workouts to Exercises with extra data (sets, reps). Stores workout-specific data that varies per session. Example: same exercise can have 3x8-10 in one workout and 4x6-8 in another.

**Why reps as String?** Supports rep ranges like "8-10", "12-15", "20+" which is standard in fitness training.

**Why PostgreSQL?** Render's free tier has an ephemeral filesystem — SQLite files would be lost on restart. PostgreSQL provides persistent storage with proper relational integrity.

**Key models:**
- `CustomUser` — extends Django's AbstractUser with bio, phone, profile picture
- `Workout` — training session with M2M to MuscleGroup and Exercise via bridge tables
- `Goal` — fitness objective, optionally linked to an Exercise, with completion tracking
- `Message` — direct message between users with read/archive flags
- `Profile` — OneToOne with CustomUser, stores profile picture (auto-created via signals)

## Local Setup

### Prerequisites
- Python 3.13+
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/Damien62-dev/fitbrigade-django.git
cd fitbrigade-django

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your values

# Run migrations
python3 manage.py migrate

# Seed the database (muscle groups and exercises)
python3 manage.py seed_db

# Create a superuser
python3 manage.py createsuperuser

# Run the development server
python3 manage.py runserver
```

Visit `http://127.0.0.1:8000`

## Environment Variables

Create a `.env` file based on `.env.example`:
```env
SECRET_KEY=your-secret-key
DEBUG=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

For production, also set:
```env
DATABASE_URL=postgresql://...
DEBUG=False
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

> **Note on Password Reset:** The password reset feature is fully implemented and functional in local development. On Render's free tier, outbound SMTP connections (ports 25, 465, 587) are blocked, preventing email delivery. A production fix would require replacing SMTP with an HTTP-based email provider such as Resend or SendGrid.

## Running Tests
```bash
python3 manage.py test
```

29 tests across workouts, goals, and messaging apps.

## Deployment on Render.com

1. Create a new **Web Service** on Render.com
2. Connect your GitHub repository
3. Set **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py seed_db && python manage.py ensure_adminuser`
4. Set **Start Command:** `gunicorn fitbrigade_project.wsgi:application --bind 0.0.0.0:$PORT`
5. Add environment variables in the Render dashboard:
   - `SECRET_KEY`
   - `DATABASE_URL` (from Render PostgreSQL)
   - `DEBUG=False`
   - `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
   - `EMAIL_HOST_USER`
   - `EMAIL_HOST_PASSWORD`
   - `DJANGO_SUPERUSER_USERNAME`
   - `DJANGO_SUPERUSER_EMAIL`
   - `DJANGO_SUPERUSER_PASSWORD`

## Project Structure
fitbrigade_django_final/
├── fitbrigade_project/     # Django project settings
├── users/                  # Authentication, profiles, signals
├── workouts/               # Workout CRUD, stats
├── goals/                  # Goals tracking
├── messaging/              # Inbox system
├── templates/              # Base HTML templates
├── static/                 # CSS, JS, images
└── media/                  # User uploaded files

## Author

Damien Mullet — Full Stack Developer Student, Dublin  
[GitHub](https://github.com/Damien62-dev)