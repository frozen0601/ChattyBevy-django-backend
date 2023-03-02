from django.test import SimpleTestCase
from django.urls import reverse, resolve
from messaging.api.views import RoomViewset

class TestUrls(SimpleTestCase):
    def test_room_url_is_resolved(self):
        url = reverse('api:my_list-list')
        print(resolve(url))