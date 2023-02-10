from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import MessageViewset, RoomViewset


router = DefaultRouter()
router.register('room', RoomViewset, basename='room')
router.register('room/(?P<bk>[^/.]+)/message',
                MessageViewset, basename='message')


urlpatterns = [
    path('', include(router.urls)),

]


# # obsolete/learning paths

# path('first/', views.firstFunction, name='firstFunction'),
# path('room/<int:>/', include(router2.urls)),
# path('view/', MessageListView.as_view(), name='messaging_list'),
# path('view/<int:pk>/', MessageDetailView.as_view(), name='messaging_detail'),
