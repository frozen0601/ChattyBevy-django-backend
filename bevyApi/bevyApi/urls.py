from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import MyTokenObtainPairView
from http import HTTPStatus
from typing import Any
from rest_framework.views import Response
from rest_framework.views import exception_handler
from rest_framework import exceptions


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # rest-auth/: for user management
    path('rest-auth/', include('dj_rest_auth.urls')),
    path('rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    # api/token/: for JWT authentication
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # messaging/: for the messaging app
    # path('messaging/', include(('messaging.api.urls', 'Message'), namespace='messaging')),
    path('messaging/', include(('messaging.api.urls', 'messaging'), namespace='messaging')),
]

def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    """Custom API exception handler."""

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, (exceptions.NotFound, exceptions.MethodNotAllowed)):
        response = Response({
            "error": {
                "status_code": exc.default_code,
                "message": exc.default_detail,
            }
        }, status=exc.status_code)
    else:
        # Call REST framework's default exception handler first,
        # to get the standard error response.
        response = exception_handler(exc, context)

    if response is not None:
        # Using the description's of the HTTPStatus class as error message.
        http_code_to_message = {v.value: v.description for v in HTTPStatus}

        error_payload = {
            "error": {
                "status_code": 0,
                "message": "",
                "details": [],
            }
        }
        error = error_payload["error"]
        status_code = response.status_code

        error["status_code"] = status_code
        error["message"] = http_code_to_message[status_code]
        error["details"] = response.data
        response.data = error_payload
    return response