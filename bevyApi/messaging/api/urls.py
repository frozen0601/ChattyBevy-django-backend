from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import MessageViewset

router = DefaultRouter()
router.register('messages', MessageViewset, basename='messages')

urlpatterns = [
    path('first/', views.firstFunction, name='firstFunction'),
    path('', include(router.urls))
]