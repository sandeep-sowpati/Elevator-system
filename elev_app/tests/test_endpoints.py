from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from elev_app.models import Building, Elevator, ElevatorRequest
from elev_app.serializers import *
import json


class BuildingAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.building_data = {'name': 'Test Building', 'max_floor': 5, 'number_of_elevators': 2}
        self.response = self.client.post(
            reverse('building'),
            self.building_data,
            format="json")

    def test_building_create(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_building_list(self):
        building = Elevator.objects.all()
        serializer = ElevatorSerializer(building,many=True)
        response = self.client.get(reverse('elevator-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_building_detail(self):
        building = Elevator.objects.first()
        response = self.client.get(reverse('elevator-detail', kwargs={'pk': building.id}))
        serializer = ElevatorSerializer(building,many=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_building_update(self):
        building = Building.objects.first()
        new_name = 'New Test Building'
        new_data = {'name': new_name}
        response = self.client.patch(
            reverse('elevator-detail', kwargs={'pk': building.id}),
            json.dumps(new_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_building_delete(self):
        building = Building.objects.first()
        response = self.client.delete(reverse('elevator-detail', kwargs={'pk': building.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Building.objects.count(), 1)

