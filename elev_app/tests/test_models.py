#unit test cases for models

#imports
from django.test import TestCase
from elev_app.models import Building, Elevator


class BuildingTestCase(TestCase):
    '''
    Unit test case for Building Model.
    '''
    def setUp(self):
        #creating the data required for Building Tescase.
        self.building = Building.objects.create(name='Test Building', max_floor=10, number_of_elevators=2)

    def test_building_str_representation(self):
        self.assertEqual(str(self.building), 'Building Test Building')

    def test_building_has_elevators(self):
        #test to check django signal elevator creation.
        self.assertEqual(self.building.elevators.count(), 2)

    def test_building_has_correct_max_floor(self):
        self.assertEqual(self.building.max_floor, 10)

    def test_building_has_correct_number_of_elevators(self):
        self.assertEqual(self.building.number_of_elevators, 2)


class ElevatorTestCase(TestCase):
    '''
    Unit test case for Elevator Model.
    '''
    def setUp(self):
        #creating the Building Object with name Test Building and with 2 elevators
        self.building = Building.objects.create(name='Test Building', max_floor=10, number_of_elevators=2)
        #getting the elevator with id = 1 , and in the given building
        self.elevator = Elevator.objects.get(building=self.building, elevator_number=1)

    def test_elevator_str_representation(self):
        self.assertEqual(str(self.elevator), 'Test Building : Elevator 1')

    def test_elevator_is_operational_by_default(self):
        self.assertTrue(self.elevator.is_operational)

    def test_elevator_current_floor_is_zero_by_default(self):
        self.assertEqual(self.elevator.current_floor, 0)

    def test_elevator_door_is_closed_by_default(self):
        self.assertFalse(self.elevator.is_door_open)

    def test_elevator_moving_status_is_idle_by_default(self):
        self.assertEqual(self.elevator.moving_status, 0)

    def test_elevator_belongs_to_building_name(self):
        self.assertEqual(self.elevator.building.name, 'Test Building')

    def test_elevator_belongs_to_building(self):
        self.assertEqual(self.elevator.building, self.building)

    def test_elevator_has_correct_number(self):
        self.assertEqual(self.elevator.elevator_number, 1)