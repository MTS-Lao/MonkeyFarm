# 🐒 Monkey Farm Management System

A web-based management system for tracking monkeys, their housing, and vaccination records, built with FastAPI, PostgreSQL, and Tailwind CSS.

## 🌟 Features

- **Auth System**
  - Secure login/logout
  - Role-based access control (Admin/Staff)
  - Token-based authentication

- **Dashboard (Admin)**
  - Entry statistics
  - Gender distribution
  - Monthly registration trends

- **Monkey Management**
  - Track monkey details (code, house/case, birthday, gender)
  - Family relationships tracking
  - Filterable list view
  - Export functionality

- **Vaccination Management**
  - Record vaccinations and doses
  - Vaccination history tracking
  - Filterable records
  - Export capabilities

- **Admin Features**
  - User management
  - House/Case management
  - System settings

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.11)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy with Alembic migrations
- **Frontend**: HTML, Tailwind CSS, Alpine.js
- **Authentication**: JWT
- **Deployment**: Docker & Easypanel compatible

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL
- Docker & Docker Compose (for deployment)

## 🚀 Getting Started

### Local Development

1. **Clone repository**
```bash
git clone [repository-url]
cd monkey-farm

2. **Set up Python environment**

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
