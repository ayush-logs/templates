Install Dependencies
--
```bash
pip install djangorestframework-simplejwt
```

Add to Installed Apps
--
```python
# settings.py

INSTALLED_APPS = [
    "rest_framework_simplejwt",
]
```

DRF Authentication Settings
--
```python
# settings.py

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}
```

JWT Configuration
--
```python
# settings.py

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),

    "AUTH_HEADER_TYPES": ("Bearer",),

    "SIGNING_KEY": SECRET_KEY,

    "AUTH_TOKEN_CLASSES": (
        "rest_framework_simplejwt.tokens.AccessToken",
    ),

    "TOKEN_TYPE_CLAIM": "token_type",
}
```
**Example Header:**
```
Authorization: Bearer <token>
```

JWT Token Views
--
```python
# urls.py

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
```

Custom Token Serializer
--
```python
# serializers.py

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email

        return token
```

Custom Login View
--
```python
# views.py

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenSerializer


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
```

**Update URL**
```python
path("api/auth/login/", CustomTokenView.as_view(), name="token_login")
```

Using Token & Refresh
--
```python
# jwt token request 
{
  "username": "admin",
  "password": "password"
}

# response
{
  "access": "access_token_here",
  "refresh": "refresh_token_here"
}

# login using the token
Authorization: Bearer <access_token>

# refreshing access token
{
  "refresh": "refresh_token"
}

# response
{
  "access": "new_access_token"
}
```