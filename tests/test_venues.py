# tests/test_venues.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_list_venues(api_client, venue_factory, user_factory):
    venue_factory.create_batch(3)
    
    admin = user_factory(is_superuser=True, is_staff=True)
    api_client.force_authenticate(user=admin)
    
    url = reverse('venues-list')
    response = api_client.get(url)
    
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_venue_superuser_only(api_client, user_factory):
    user = user_factory()
    api_client.force_authenticate(user=user)
    
    url = reverse('venues-list')
    data = {"name": "New Arena", "location": "POINT(30 60)"}
    
    response = api_client.post(url, data)
    assert response.status_code == 403
    
    admin = user_factory(is_superuser=True, is_staff=True)
    api_client.force_authenticate(user=admin)
    
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data['name'] == "New Arena"
