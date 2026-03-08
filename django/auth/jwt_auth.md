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

# Theory

- **Header:** algorithm + token type
- **Payload:** contains the claims. Claims are statements about the user (like user ID, user roles, expiration time, etc.). There are three types of claims: registered, public, and private.
- **Signature:** To create the signature, you must take the encoded header, the encoded payload, and a secret key and sign that using the algorithm specified in the header.

```md
HMACSHA256(  
	base64(header) + "." + base64(payload),  
	secret_key  
)
```

### Flow Diagram
![Flow Diagram](https://coredevsltd.com/articles/wp-content/uploads/2023/10/the-flow-diagram-for-JWT-Authentication-in-the-context-of-Asp.net-Core-Web-API.png)

### Algorithm
- A user provides valid credentials, triggering the server to generate a JWT token.
- The server sends the token to the client, who stores it securely.
- The client includes the token in the headers of subsequent requests.
- The server validates the token’s authenticity and integrity.
- If valid, the server extracts claims to identify the user and their permissions.
- The server grants or denies access based on the extracted claims.
- If tokens expire, the client can request a new token using a refresh token.
- Tokens can be revoked on the server if necessary.

