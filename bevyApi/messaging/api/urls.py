from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import MessageViewset, MessageListView, MessageDetailView, RoomViewset


router = DefaultRouter()
router.register('room', RoomViewset, basename='room')
# router2.register('message', MessageViewset, basename='message')
router.register('room/(?P<bk>[^/.]+)/message', MessageViewset, basename='message')


urlpatterns = [
    # path('first/', views.firstFunction, name='firstFunction'),
    path('', include(router.urls)),
    # path('room/<int:>/', include(router2.urls)),
    # path('view/', MessageListView.as_view(), name='messaging_list'),
    # path('view/<int:pk>/', MessageDetailView.as_view(), name='messaging_detail'),
]
