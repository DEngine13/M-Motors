# M-Motors — Vehicle Rental Platform

Web application for M-Motors, a used car dealership adding a long-term rental service with purchase option.

**Live application:** https://dh-m-motors.up.railway.app/

Demo credentials are provided in the project documentation (PDF).

## Motivation

M-Motors is the capstone project of the Bachelor *Concepteur Développeur de Solutions Digitales (Python)*. It simulates a real-world brief: an established used-car dealership (~1,000,000 customers, 800 employees) wants to launch a long-term rental service with purchase option, and needs its web application rebuilt from the ground up.

The goal was to deliver a complete, production-grade solution end to end — not just feature code, but the full lifecycle around it:

- A client-facing catalog, account system, and 100% paperless application flow
- A back-office for staff to manage vehicles and process applications
- Automated testing (unit, integration, E2E) with enforced coverage
- Continuous integration and automated deployment to the cloud
- Security hardening, logging, and monitoring

It was built solo, one line at a time, as a demonstration of the ability to ship and operate a real Django application under real constraints.

## Tech Stack

- **Backend:** Django 6.0.3, Python 3.13
- **Frontend:** Django Templates, Bootstrap 5, JavaScript
- **Database:** PostgreSQL (production), SQLite (development)
- **Deployment:** Railway PaaS, Gunicorn, WhiteNoise
- **CI/CD:** GitHub Actions (flake8 linting + pytest)
- **Testing:** pytest + pytest-cov (83% coverage), Playwright (E2E)
- **Monitoring:** Python logging (console handler)

## Quick Start

For those who just want it running locally (Python 3.13+ and Git required):

```bash
# 1. Clone and enter the project
git clone https://github.com/DEngine13/M-Motors.git
cd M-Motors

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file with a secret key and debug mode
echo "SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" > .env
echo "DEBUG=True" >> .env

# 5. Set up the database and load demo data
python manage.py migrate
python manage.py migrate_data

# 6. Run the server
python manage.py runserver
```

Then open http://127.0.0.1:8000/. See [Getting Started](#getting-started) below for a step-by-step walkthrough.

## Getting Started

### Prerequisites

- Python 3.13+
- Git

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/DEngine13/M-Motors.git
   cd M-Motors
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

## Usage

The application has two sides: the public/client interface and the staff back-office.

### Client interface

1. **Browse the catalog** at the home page. Filter vehicles by brand, offer type (sale / rental), maximum price, and maximum mileage.
2. **Open a vehicle** to see its full details, photos, and pricing.
3. **Create an account** (name, email, phone, address) to be able to submit an application.
4. **Submit an application** from a vehicle page:
   - *Purchase* — starts the acquisition request directly.
   - *Rental* — choose a duration (12, 24, 36, or 48 months) and optional services (insurance, roadside assistance, maintenance, technical inspection); the monthly total updates live.
5. **Upload documents** one by one to complete the paperless file: ID card, proof of address, three payslips, and bank details (RIB). Accepted formats: PDF, JPG, PNG (5 MB max per file).
6. **Track progress** from the dashboard: each application shows its vehicle, type, date, and status (Awaiting processing → In review → Approved / Rejected).

### Back-office (staff)

Accessible at `/admin/` with an administrator account.

- **Vehicles:** add, edit, toggle a vehicle between sale and rental, or deactivate it (soft delete — it disappears from the public catalog but its applications remain).
- **Rental options:** manage the services offered with rental subscriptions.
- **Applications:** list, filter (by status, type, date) and search (by client name, email, or vehicle); review the uploaded documents inline.
- **Process applications:** mark an application as In Review, Approved, or Rejected. Each status change sends an email notification to the client (a reason is included for rejections).
- **Users:** manage client accounts and their information.

## Running Tests

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

## Contributing

This is a completed academic project, but contributions and suggestions are welcome. The workflow mirrors the one used throughout development:

1. **Fork** the repository and create your branch from `develop`:

   ```bash
   git checkout develop
   git checkout -b feature/short-description
   ```

2. **Write code and tests.** Every new feature or fix should be covered by tests. Overall coverage must stay at or above 80%.

3. **Check style and tests locally** before pushing:

   ```bash
   flake8 accounts vehicles applications --max-line-length=120 --exclude=migrations
   pytest --cov-fail-under=80 --ignore=tests/test_e2e.py
   ```

4. **Open a Pull Request** targeting `develop`. The GitHub Actions pipeline (flake8 + pytest) must pass before a merge is considered.

5. After review and validation on `develop`, changes are merged into `main`, which triggers automatic deployment to Railway.

Please keep commits focused and use clear, conventional messages (e.g. `feat:`, `fix:`, `test:`, `docs:`).

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
