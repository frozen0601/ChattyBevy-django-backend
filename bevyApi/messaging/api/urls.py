from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewset, RoomViewset

router = DefaultRouter()
router.register('room', RoomViewset, basename='room')
router.register('room/(?P<room_id>[^/.]+)/message',
                MessageViewset, basename='message')


urlpatterns = [
    path('', include(router.urls)),

]
