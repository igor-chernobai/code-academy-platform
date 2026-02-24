# Academy Course Platform API & Web

A production-ready online education platform backend built with Django and Django REST Framework. This project implements a complex subscription-based access model, student progress tracking, and robust infrastructure using Docker orchestration.

## 🌟 Key Business Logic
* **Custom Email-Based Authentication:** Extended Django's `AbstractUser` to use `Email` as the primary identifier instead of `Username`, following modern security and UX standards.
* **Dual Authentication System:** Integrated support for both `SimpleJWT` (with blacklist) and `DRF Token Authentication` for maximum client compatibility.
* **Flexible Subscription Model:** Role-based access control (RBAC) where lesson availability is dynamically checked based on the student's active subscription plan.
* **Progress Tracking Service:** Custom Service Layer logic to monitor student activity, lesson completion status, and unlock logic for subsequent modules.
* **Complex Permissions:** Granular access levels using custom permission classes (`HasActiveSubscription`, `IsEnrolled`, `IsAdminOrReadOnly`).
* **Performance Optimization:** Implemented server-side caching using Django's Cache Framework (Redis-ready) to optimize plan retrieval and course listings.

## 🛠 Tech Stack
* **Backend:** Python 3.12, Django 5.2
* **API:** Django REST Framework (DRF), SimpleJWT
* **Database:** PostgreSQL 16 (Relational design with focus on integrity)
* **Infrastructure:** Docker & Docker Compose
* **Web Server:** Gunicorn & Nginx (serving as a Reverse Proxy)
* **Frontend Integration:** Tailwind CSS via PostCSS

## 🐳 Containerization & Infrastructure
The application is fully containerized to ensure "build once, run anywhere" consistency:
* **Multi-Environment Orchestration:**
    * `compose.dev.yml`: Optimized for development with hot-reload.
    * `compose.prod.yml`: Security-hardened for deployment.
* **Nginx Reverse Proxy:** Configured for efficient static/media file delivery and request proxying to Gunicorn.
* **Healthchecks:** Implemented database-readiness checks to ensure the backend starts only when PostgreSQL is fully operational.
* **Persistent Storage:** Configured Docker Volumes for database persistence and user-uploaded media.

## ⚙️ Installation & Setup

1. **Clone the repository:**
```bash
git clone [https://github.com/Igor231321/code-academy-platform.git](https://github.com/Igor231321/code-academy-platform.git)
cd code-academy-platform
```

2. **Configure Environment:**
Create your production environment file from the template:

```bash
cp .env.example .env.prod
# Open .env.prod and fill in your DB_PASSWORD and SECRET_KEY
```


3. **Deploy using Docker Compose:**

```bash
docker-compose -f compose.prod.yml up -d
```

## 🌍 Accessing the Application

Once the containers are successfully running, you can access the platform services at:

* **💻 Web Interface:** [http://localhost](http://localhost)
* **🔐 Admin Panel:** [http://localhost/admin/](http://localhost/admin/)
* **🔌 API Entry Point:** [http://localhost/api/](http://localhost/api/)

## 🔌 API Endpoints (Quick Overview)

* `POST /api/token/` — Obtain JWT access/refresh pair.
* `GET /api/courses/` — List courses with search/filter/ordering.
* `POST /api/courses/{id}/enroll/` — Enroll in a course (Requires active plan).
* `GET /api/course/{id}/lesson/{slug}/` — Access protected lesson content with activity tracking.

## 📈 Roadmap

* [ ] Integration with Stripe/Braintree for automated billing.
* [ ] Increase test coverage to 90%+ using Pytest.
* [ ] Implement Celery + Redis for asynchronous email processing.
