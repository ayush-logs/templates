"""
PostgreSQL Database Configuration Template
==========================================

Purpose
-------
Standardized configuration for connecting Django to PostgreSQL.

Design Decisions
----------------
1. Environment variables are used for all credentials.
2. No secrets are stored in source control.
3. Supports both local development and production.
4. Compatible with containerized deployments (Docker/Kubernetes).
5. Optional connection pooling settings included.

Required Packages
-----------------
pip install psycopg2-binary

Environment Variables Example
---------------------
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT

# Optional
DB_CONN_MAX_AGE=60
"""

import os


# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

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

# ==========================================================
# SETTINGS CONFIGURATION
# ==========================================================
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
