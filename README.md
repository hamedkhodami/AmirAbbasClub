# 🏋️ AmirAbbasClub – Gym Automation System

A minimal yet powerful automation system for managing gym memberships and fees, built with **Django Templates**.  
The project is designed around three core roles: **Athlete, Coach, and Superuser**.

---

## 🎯 Project Goals
- Simplify membership management for gym athletes.
- Allow coaches to register athletes and track fee payments.
- Provide superusers with full control, including income reports and coach management.
- Deliver a clean, minimal interface using Django Admin and Templates.

---

## 👥 Roles & Permissions

### Athlete
- Registered only by a coach or superuser.
- Basic information: first name, last name, phone number, national ID, address.
- No direct access to the system.

### Coach
- Register new athletes.
- View athlete list and payment status.
- **Limitation:** Cannot view overall gym income.

### Superuser
- All coach capabilities.
- View total gym income (sum of payments).
- Manage coaches (add/remove).
- Full access to reports and database.

---

## 🛠 Tech Stack & Tools

### Backend
- **Django (Python)** – Core framework for building the application.
- **Django Templates** – Simple and fast server-side rendering.
- **Django Admin** – Built-in admin panel for managing users, payments, and reports.

### Frontend
- **HTML5 / CSS3 / JavaScript (ES6+)** – Base technologies for templates.
- **TailwindCSS** – Utility-first CSS framework for a clean, minimal design.
- **Alpine.js** (optional) – Lightweight JavaScript for interactivity in templates.

### Database
- **SQLite** – For local development and testing.
- **PostgreSQL** – For production deployment (secure and scalable).

### Development Tools
- **Django Debug Toolbar** – Debugging and performance insights.
- **Black & Flake8** – Code formatting and linting.
- **Git + GitHub** – Version control and collaboration.

### Deployment
- **Docker** – Containerized environment (optional).
- **Gunicorn + Nginx** – Production-ready server setup.
- **GitHub Actions** – CI/CD pipeline for automated testing and deployment.

---