Project: Cyber Security Base — Course Project 1

# Installation

Prerequisites:
- Python 3.8 or newer
- Git (optional)

1. Clone the repository and navigate into the project directory:

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply database migrations and create a superuser if needed:

```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

6. Run tests:

```bash
python manage.py test
```
