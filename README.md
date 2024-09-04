# simple-chat

We need to provide an application with 2 models:
1. Thread (fields - participants, created, updated)
2. Message (fields - sender, text, thread, created, is_read)

Thread can’t have more than 2 participants.

## Endpoints

- Create thread: `/api/threads/` (POST)
- Delete thread: `/api/threads/<id>/` (DELETE)
- List threads: `/api/threads/list/` (GET)
- Create message: `/api/messages/` (POST)
- List messages: `/api/threads/<thread_id>/messages/` (GET)
- Mark message as read: `/api/messages/<message_id>/read/` (POST)
- Unread message count: `/api/messages/unread_count/` (GET)

## Setup

1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Create a superuser: `python manage.py createsuperuser`
6. Run the server: `python manage.py runserver`

## Development

Create a virtual environment:
`python3 -m venv env`

Activate virtual environment:
`source env/bin/activate`

Install Django and Django REST Framework:
`pip install django djangorestframework djangorestframework-simplejwt'

Run Migrations and Create Superuser:
`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py createsuperuser`

Create Database Dump:
`python manage.py dumpdata --natural-foreign --indent 4 > db.json`

Tests:
`python manage.py test`
