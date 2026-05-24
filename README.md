# M-Motors — Vehicle Rental Platform

Web application for M-Motors, a used car dealership adding a long-term rental service with purchase option.

**Live application:** https://dh-m-motors.up.railway.app/

Demo credentials are provided in the project documentation (PDF).

## Tech Stack

- **Backend:** Django 6.0.3, Python 3.13
- **Frontend:** Django Templates, Bootstrap 5, JavaScript
- **Database:** PostgreSQL (production), SQLite (development)
- **Deployment:** Railway PaaS, Gunicorn, WhiteNoise
- **CI/CD:** GitHub Actions (flake8 linting + pytest)
- **Testing:** pytest + pytest-cov (83% coverage), Playwright (E2E)
- **Monitoring:** Python logging (console handler)

### Prerequisites

- Python 3.13+
- Git

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/DEngine13/M-Motors.git
   cd M-Motors-main
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv

   # Windows (PowerShell)
   venv\Scripts\Activate.ps1

   # Windows (Git Bash / CMD)
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file at the project root (same level as `manage.py`):

   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

   Generate a secret key with:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. Apply migrations:

   ```bash
   python manage.py migrate
   ```

6. Load demo data (12 vehicles, 4 rental options, admin and client accounts):

   ```bash
   python manage.py migrate_data
   ```

   **Note:** Demo data does not include vehicle photos. Photos can be added via the admin panel at http://127.0.0.1:8000/admin/.

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

8. Open http://127.0.0.1:8000/ in your browser.

### Unit and integration tests (46 tests, 83% coverage)

```bash
pytest
```

### E2E tests with Playwright (4 tests)

E2E tests require a running server and a browser. They are excluded from CI.

```bash
# Install browser (first time only)
playwright install chromium

# In a first terminal, start the server
python manage.py runserver

# In a second terminal, run E2E tests
pytest tests/test_e2e.py -v

# To see the browser in action
pytest tests/test_e2e.py -v --headed --slowmo 500
```

## Project Structure

```
M-Motors/
├── accounts/                          # User model, signup, signin, profile, dashboard
│   ├── templates/accounts/            # 8 templates (signin, signup, profile, dashboard, password reset)
│   ├── admin.py                       # UserAdmin with phone and address fields
│   ├── forms.py                       # SignUpForm (extends UserCreationForm)
│   ├── models.py                      # Custom User model (AbstractUser + phone, address)
│   ├── urls.py                        # Auth URLs + password reset (4 views)
│   └── views.py                       # signup, signin, logout, profile, dashboard
│
├── applications/                      # Purchase and rental applications
│   ├── templates/applications/        # 4 templates (apply purchase/rental, upload, detail)
│   ├── admin.py                       # ApplicationAdmin with actions + email notifications
│   ├── models.py                      # Application model + Document model
│   ├── urls.py                        # Apply, upload documents, application detail
│   └── views.py                       # apply_purchase, apply_rental, upload_documents, detail
│
├── vehicles/                          # Vehicle catalog and rental options
│   ├── management/commands/           # migrate_data.py (seed command)
│   ├── templates/vehicles/            # 3 templates (vehicle_list, vehicle_details, rental_options)
│   ├── admin.py                       # VehicleAdmin with toggle/activate actions + RentalOptionAdmin
│   ├── models.py                      # Vehicle model + RentalOption model
│   ├── urls.py                        # Catalog, vehicle detail, rental options page
│   └── views.py                       # vehicle_list (with filters), vehicle_detail, rental_options_page
│
├── config/                            # Django project configuration
│   ├── settings.py                    # Settings with .env, logging, Sentry-ready
│   ├── urls.py                        # Root URL routing + media file serving
│   └── wsgi.py                        # WSGI entry point (Gunicorn)
│
├── static/images/                     # MM_Logo.png, MM_Favicon.png
├── tests/                             # test_models.py, test_views.py, test_e2e.py
├── .github/workflows/ci.yml          # CI pipeline (flake8 + pytest)
├── .env                               # Environment variables (not versioned)
├── .gitignore
├── Procfile                           # Railway start command
├── pytest.ini                         # Pytest configuration
├── requirements.txt                   # Python dependencies
└── manage.py
```

## Git Workflow

- `main` — stable production branch
- `develop` — integration branch
- `feature/us-xxx` — feature branches per user story

## Deployment (Railway)

**Build command:**

```
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

**Start command (Procfile):**

```
python manage.py migrate && python manage.py migrate_data && gunicorn config.wsgi --bind 0.0.0.0:$PORT
```

### Required environment variables

| Variable               | Example                               |
| ---------------------- | ------------------------------------- |
| `SECRET_KEY`           | (generated Django key)                |
| `DEBUG`                | `False`                               |
| `DATABASE_URL`         | (auto-injected by Railway PostgreSQL) |
| `ALLOWED_HOSTS`        | `your-app.up.railway.app`             |
| `CSRF_TRUSTED_ORIGINS` | `https://your-app.up.railway.app`     |
| `PYTHONUNBUFFERED`     | `1`                                   |
