# Dynamic Profile Endpoint

Small Django project that exposes a single endpoint, `/me`, which returns a JSON payload:

- status: always "success"
- user: { email, name, stack }
- timestamp: current UTC time in ISO 8601 format
- fact: a random cat fact fetched from https://catfact.ninja/fact (with graceful fallback)

This README covers quick setup, installation, running, testing instructions for Windows using bash, and how to use a `.env` file.

Prerequisites
- Python 3.10+ installed and available on PATH
- Git (optional)

Setup and installation (Windows, bash)

1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/Scripts/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Apply database migrations

```bash
python manage.py migrate
```

Run the development server

```bash
python manage.py runserver
```

Open the endpoint in your browser or with curl:

```bash
curl http://127.0.0.1:8000/me
```

Testing

Run the project's unit tests:

```bash
python manage.py test
```

Using a .env file (recommended for local secrets)

1) Create a file named `.env` in the project root. Example contents:

```env
# .env (example)
DEBUG=True
SECRET_KEY=changeme_local_secret_key
CATFACT_TIMEOUT=2  # seconds to wait for the external API
MY_EMAIL=you@example.com
MY_NAME=Your Name
MY_STACK=Python/Django
```

2) Loading the .env in Django

- Option A — python-dotenv (simple): add to `requirements.txt` and load early in `manage.py` or `Profile/settings.py`:

```python
from dotenv import load_dotenv
load_dotenv()  # loads variables from .env into os.environ
```

- Option B — django-environ (recommended for Django apps):

```python
import environ
env = environ.Env()
environ.Env.read_env()  # reads .env

# usage
DEBUG = env.bool('DEBUG', default=False)
SECRET_KEY = env('SECRET_KEY')
```

3) Accessing .env variables in your code

Use `os.environ.get('MY_EMAIL')` or via the `env` helper when using `django-environ`.

Security notes
- Do not commit `.env` to version control. Add `.env` to `.gitignore` (already included in this repo's `.gitignore`).
- For production, use real secret management (Azure Key Vault, AWS Secrets Manager, Vault, or environment variables set by the hosting platform) instead of `.env` files.

Notes and troubleshooting

- The project uses SQLite by default (`db.sqlite3`) for local development. The database file is small and intended only for local testing.
- The `/me` endpoint fetches a cat fact from the Cat Facts API. If the external API is unavailable or times out, the endpoint should return a fallback message in the `fact` field and still return HTTP 200.
- For repeatable tests, mock external HTTP calls using `unittest.mock` or libraries like `responses` or `requests-mock`.
- If you see permission errors activating the virtual environment on Windows, run the bash shell as administrator or configure execution policy appropriately.

Contact / author

Add your name, email, and preferred backend stack into the `/me` view's `user` payload if you want it personalized for your deployments.
