from django.urls import path, include
from . import views
from http import HTTPStatus
from typing import Any
from rest_framework.routers import DefaultRouter
from rest_framework.views import Response
from .views import MessageViewset, RoomViewset
from rest_framework.views import exception_handler
from rest_framework import exceptions



router = DefaultRouter()
router.register('room', RoomViewset, basename='room')
router.register('room/(?P<bk>[^/.]+)/message',
                MessageViewset, basename='message')


urlpatterns = [
    path('', include(router.urls)),

]

def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Response:
    """Custom API exception handler."""
    if isinstance(exc, exceptions.APIException):
        response = Response(data={
            "error": {
                "status_code": exc.status_code,
                "message": exc.default_detail,
                "details": [],
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
