# 🏋️ AmirAbbasClub – Gym Automation System

A minimal yet powerful automation system for managing gym memberships and fee tracking, built with **Django** and **TailwindCSS**.  
Designed for three core roles: **Athlete**, **Coach**, and **Superuser**, the system streamlines registration, payment tracking, and administrative oversight.

---

## 🎯 Project Goals

- ✅ Simplify athlete registration and fee management.
- ✅ Empower coaches to manage their athletes and monitor payments.
- ✅ Provide superusers with full administrative control and income reporting.
- ✅ Deliver a clean, responsive UI using Django Templates and TailwindCSS.
- ✅ Ensure maintainability through clean code, modular design, and automated testing.

---

## 👥 Roles & Permissions

### 🧍 Athlete
- Registered by a coach or superuser.
- Stores personal info: name, phone, national ID, address.
- No login or direct access to the system.

### 🧑‍🏫 Coach
- Can register new athletes.
- Views list of athletes and their payment status.
- **Restricted** from viewing total gym income or managing other coaches.

### 🛡️ Superuser
- Full access to all system features.
- Manages coaches and athletes.
- Views total income reports and payment summaries.
- Access to Django Admin and all backend tools.

---

## 🛠 Tech Stack & Tools

### ⚙️ Backend
- **Django (Python)** – Robust web framework for rapid development.
- **Django Templates** – Server-side rendering for dynamic HTML.
- **Django Admin** – Admin interface for managing users, payments, and reports.

### 🎨 Frontend
- **TailwindCSS** – Utility-first CSS framework for responsive, RTL-friendly design.
- **HTML5 / CSS3 / JavaScript (ES6+)** – Core technologies for templating and interactivity.
- **Alpine.js** *(optional)* – Lightweight JS for modals, toggles, and dynamic UI behavior.

### 🗄️ Database
- **SQLite** – Lightweight DB for development and testing.
- **PostgreSQL** – Production-grade database for deployment.

### 🧰 Development Tools
- **Black / Flake8 / isort** – Code formatting and linting.
- **Django Debug Toolbar** – In-browser debugging and SQL inspection.
- **Pre-commit Hooks** – Enforce code quality before commits.
- **Git + GitHub** – Version control and collaboration.

### 🚀 Deployment Stack
- **Gunicorn** – WSGI HTTP server for running Django in production.
- **Nginx** – Reverse proxy and static file server.
- **Supervisor** – Process manager for Gunicorn.
- **GitHub Actions** – CI/CD pipeline for testing and deployment.

---
