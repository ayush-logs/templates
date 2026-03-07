# .env Configuration Template

**Design Decisions**
---
1. Environment variables are used for all credentials.
2. No secrets are stored in source control.
3. Supports both local development and production.
4. Compatible with containerized deployments (Docker/Kubernetes).
5. Optional connection pooling settings included.

**Required Packages**
---
```python
pip install dotenv
```

**Environment Variables**
---
```python
# ==========================================================
# DJANGO CORE SETTINGS
# ==========================================================

# Set to False in production
DEBUG=True

# Comma separated list of allowed hosts
# Example: example.com,www.example.com
ALLOWED_HOSTS=127.0.0.1,localhost


# ==========================================================
# DJANGO SECURITY
# ==========================================================

# Generate using:
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY=replace_me_with_secure_key


# ==========================================================
# DATABASE (POSTGRESQL)
# ==========================================================

DB_NAME=myproject_db
DB_USER=myproject_user
DB_PASSWORD=strongpassword
DB_HOST=localhost
DB_PORT=5432

# Connection pooling
DB_CONN_MAX_AGE=60


# ==========================================================
# DJANGO ADMIN
# ==========================================================

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=adminpassword


# ==========================================================
# CORS (FOR FRONTEND APPS LIKE REACT)
# ==========================================================

# Example:
# http://localhost:3000
# https://yourfrontend.com
CORS_ALLOWED_ORIGINS=http://localhost:3000


# ==========================================================
# EMAIL (OPTIONAL)
# ==========================================================

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=password
EMAIL_USE_TLS=True


# ==========================================================
# REDIS (OPTIONAL - CACHING / CELERY)
# ==========================================================

REDIS_URL=redis://127.0.0.1:6379/1


# ==========================================================
# LOGGING
# ==========================================================

LOG_LEVEL=INFO


# ==========================================================
# FILE STORAGE (OPTIONAL)
# ==========================================================

MEDIA_ROOT=media/
STATIC_ROOT=staticfiles/


# ==========================================================
# THIRD PARTY SERVICES (OPTIONAL)
# ==========================================================

# Example placeholders for external integrations

STRIPE_SECRET_KEY=
STRIPE_PUBLIC_KEY=

SENTRY_DSN=
```

**Imports**
---
```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
```

**Project Settings Configuration**
---
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # Database name
        "NAME": os.getenv("DB_NAME", "postgres"),
        # Database username
        "USER": os.getenv("DB_USER", "postgres"),
        # Database password
        "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
        # Host (localhost for dev, container/db host for production)
        "HOST": os.getenv("DB_HOST", "localhost"),
        # PostgreSQL default port
        "PORT": os.getenv("DB_PORT", "5432"),
        # Connection behavior
        "CONN_MAX_AGE": int(os.getenv("DB_CONN_MAX_AGE", 60)),
        # Optional: Improve connection reliability
        "OPTIONS": {
            "connect_timeout": 10,
        },
    }
}
```


