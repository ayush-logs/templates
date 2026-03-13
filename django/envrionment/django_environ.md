# Django-Environ Setup Template

## 1. Install Dependency

```bash
pip install django-environ
```

---

# 2. Create `.env` File

Example:

```env
DEBUG=True
SECRET_KEY=replace_with_secure_secret

ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=myproject_db
DB_USER=myproject_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

---

# 3. Setup in `settings.py`

```python
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# Read .env file
environ.Env.read_env(BASE_DIR / ".env")

DEBUG = env("DEBUG")

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
```

---

# 4. PostgreSQL Database Configuration

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}
```

---

# 5. Boolean Example

```python
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
```

---

# 6. Integer Example

```python
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
```

---

# 7. List Example

```python
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
```

`.env`

```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

# 8. Optional: Database URL Pattern

`django-environ` also supports full database URLs.

`.env`

```env
DATABASE_URL=postgres://user:password@localhost:5432/mydb
```

Settings:

```python
DATABASES = {
    "default": env.db()
}
```

---

# 9. `.gitignore` Rule

Ensure `.env` is ignored.

```gitignore
.env
.env.*
!.env.example
```

---

# 10. `.env.example` Template

Commit this to the repo:

```env
DEBUG=True
SECRET_KEY=replace_me

ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=myproject_db
DB_USER=myproject_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

---

# Design Decisions (Why This Template Works)

### Environment-based configuration

Keeps secrets out of source control.

### Type casting

Avoids mistakes like:

```python
DEBUG = "False"  # incorrect
```

### Consistent configuration

Works across:

* local development
* Docker
* cloud deployments
	
