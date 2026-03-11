Design Decisions
--
**Pros:**
1. Simple to implement
2. Works well for small APIs
3. No refresh token complexity

**Cons**
1. Stateful
2. Tokens never expire by default
3. Harder to scale
4. Less secure than JWT for public APIs

Implement in 5 Steps
--
1. add `rest_framework.authtoken` to installed apps. 
2. migrate -> creates `authtoken_token` table. 
3. configure default `authentication` and `permission` class in settings. 
4. add login endpoint : : `from rest_framework.authtoken.views import obtain_auth_token`
5. add logout endpoint : : `request.user.auth_token.delete()`

Add Token App
--
```
# settings.py

INSTALLED_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
]
```

Run Migrations
--
```
python manage.py migrate
```

DRF Authentication Configuration
--
```
# settings.py

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}
```

**Design Decision**
1. All APIs require authentication by default. 
2. Public endpoints must explicitly override permissions.

Generate Token for User
--
```
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()

user = User.objects.get(email="user@example.com")
token, created = Token.objects.get_or_create(user=user)

print(token.key)
```

Authentication Header
--
```
Authorization: Token <token_key>
```

Token Login Endpoint
--
```
# urls.py

from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

urlpatterns = [
    path("api/auth/token/", obtain_auth_token),
]
```

**Example**
```python
{
  "username": "admin",
  "password": "password"
}

# RESPONSE
{
  "token": "6a2d9f8b6e9c2e87d8e0..."
}
```

Auto Create Token on User Creation
--
```
# signals.py

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
```

> Register signals in `apps.py`.

Logout
--
```
def logout(request):
    request.user.auth_token.delete()
    
```
