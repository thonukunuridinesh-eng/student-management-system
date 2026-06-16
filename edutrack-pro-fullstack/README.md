# EduTrack Pro - Student Management System

EduTrack Pro is a full-stack Student Management System built with Django REST Framework, PostgreSQL-ready settings, JWT authentication, React, Vite, Tailwind CSS, Axios, React Router, and Framer Motion.

## Features

- JWT login, refresh, logout, and profile APIs
- Admin, teacher, and student roles
- Department, teacher, student, course, enrollment, attendance, grade, and notice models
- Role-based API filtering
- Django Admin setup
- Responsive React dashboard
- Render backend deployment config
- Vercel frontend config

## Tech Stack

- Backend: Python, Django, Django REST Framework, Simple JWT
- Database: SQLite for quick local run, PostgreSQL for production
- Frontend: React, Vite, Tailwind CSS, Axios, React Router, Framer Motion
- Deployment: Render, Vercel, GitHub

## Local Backend Setup

```powershell
cd projects\student-management-system\backend
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py seed_sample_data
python manage.py runserver 127.0.0.1:8001
```

Backend URL:

```text
http://127.0.0.1:8001
```

## Local Frontend Setup

```powershell
cd projects\student-management-system\frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Frontend URL:

```text
http://127.0.0.1:5174
```

## Demo Accounts

```text
Admin:   admin@edutrack.com / Admin@12345
Teacher: teacher@edutrack.com / Teacher@12345
Student: student@edutrack.com / Student@12345
```

## API Endpoints

```text
POST   /api/auth/register/
POST   /api/auth/login/
POST   /api/auth/token/refresh/
POST   /api/auth/logout/
GET    /api/auth/me/
GET    /api/students/dashboard/
CRUD   /api/students/departments/
CRUD   /api/students/teachers/
CRUD   /api/students/profiles/
CRUD   /api/students/courses/
CRUD   /api/students/enrollments/
CRUD   /api/students/attendance/
CRUD   /api/students/grades/
CRUD   /api/students/notices/
```

## Postman Testing

1. Start the backend server.
2. Send `POST http://127.0.0.1:8001/api/auth/login/`.
3. Use this body:

```json
{
  "email": "admin@edutrack.com",
  "password": "Admin@12345"
}
```

4. Copy the `access` token.
5. Add `Authorization: Bearer <access_token>` to protected requests.
6. Test dashboard and CRUD endpoints.

## Render Deployment

1. Push this project to GitHub.
2. Create a Render Blueprint or Web Service.
3. Use `projects/student-management-system/backend` as the backend root if creating manually.
4. Add environment variables:

```text
SECRET_KEY
DEBUG=False
ALLOWED_HOSTS
CORS_ALLOWED_ORIGINS
CSRF_TRUSTED_ORIGINS
DATABASE_URL
```

5. Build command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

6. Start command:

```bash
gunicorn config.wsgi:application
```

## Vercel Deployment

1. Import the GitHub repository into Vercel.
2. Set root directory to `projects/student-management-system/frontend`.
3. Add environment variable:

```text
VITE_API_BASE_URL=https://your-render-backend-url.onrender.com/api
```

4. Deploy.

## Resume Bullets

- Built a full-stack student management platform using Django REST Framework, React, PostgreSQL-ready configuration, and JWT authentication.
- Implemented role-based access control for admins, teachers, and students across protected REST APIs.
- Designed normalized database models for departments, courses, enrollments, attendance, grades, and notices.
- Deployed a production-ready backend/frontend architecture using Render, Vercel, and GitHub.

## Interview Explanation

EduTrack Pro separates authentication, academic records, and role-based access. Admins manage master data, teachers manage attendance and grades for assigned courses, and students can view only their own academic data. The backend uses DRF ViewSets, serializers, model validation, JWT authentication, and custom permissions. The frontend uses protected routes, Axios token headers, and responsive Tailwind pages.
