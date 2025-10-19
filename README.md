# Event Manager API

A Django REST API for managing events — including CRUD operations, user authentication, and event registration.

## Features

- User registration and login
- Event creation, update, and deletion
- Upcoming events list
- Event capacity limits

## Tech Stack

- Python 3
- Django & Django REST Framework
- SQLite (dev)
- JWT Auth (optional)

## Setup

```bash
git clone git clone https://github.com/brianroba/Event-Management.git
cd event-manager-api
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
