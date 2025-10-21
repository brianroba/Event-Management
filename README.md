# Event Manager API

A Django REST API for managing events — including CRUD operations, user authentication, and event registration.

## Features

- User registration and login
- Event creation, update, and deletion
- View upcoming events
- Event capacity management

## Tech Stack

- **Backend:** Python 3, Django, Django REST Framework
- **Database:** SQLite (for development)
- **Authentication:** JWT (optional)

## Setup Instructions

1. Clone the repository:
   Git bash
   git clone https://github.com/brianroba/Event-Management.git
   cd Event-Management

2. Set up a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
3. Install dependencies:
   pip install -r requirements.txt

4. Apply migrations:
   python manage.py migrate

5. Run the development server:
   python manage.py runserver - The API will be available at http://127.0.0.1:8000/

6. API Endpoints:
	Method	   Endpoint	       Description
	POST	/api/register/	    Register a new user
	POST	/api/login/	        User login
	GET		/api/events/	    List all upcoming events
	POST	/api/events/	    Create a new event (Admin only)
	PUT	    /api/events/{id}/	    Update an existing event (Admin only)
	DELETE	/api/events/{id}/	Delete an event (Admin only)

7. Authentication
  JWT authentication is optional. To enable it:
  -Install djangorestframework-simplejwt
  -Configure JWT in your Django settings

8. Contributing
   Feel free to fork the repository, submit issues, or open pull requests. Contributions are welcome!
