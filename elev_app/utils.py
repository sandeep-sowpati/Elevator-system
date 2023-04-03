
from .models import Elevator,ElevatorRequest,Building
from threading import Thread

class RunThread(Thread):
  '''
  A different thread running in an infinite loop
  to process all the requests made to an elevator
  '''
  def run(self):
    while True:
      final_run()



def move_elevator(elevator_object : Elevator,building : Building):
  '''
  Filter all the requests for a given elevator
  move it according to the requests.
  '''
  requests_pending = ElevatorRequest.objects.filter(
    elevator = elevator_object,
    is_active = True,
  ).order_by('request_time')

  for elev_request in requests_pending:
    request_start = elev_request.requested_floor
    request_destination = elev_request.destination_floor
    curr_elev_location = elevator_object.current_floor


    # Close the door
    elevator_object.is_door_open = False

    # Go to starting point
    if request_start > curr_elev_location:
      # Start going up
      elevator_object.moving_status = 1
    elif request_start < curr_elev_location:
      # Start going down
      elevator_object.moving_status = -1
    elevator_object.save()

    # Destination reached, stop running
    # Open the door
    elevator_object.current_floor = request_start
    elevator_object.moving_status = 0
    elevator_object.is_door_open = True
    elevator_object.save()

    # Let people get in, Close the door
    elevator_object.is_door_open = False
    if request_destination > curr_elev_location:
      # Start going up
      elevator_object.moving_status = 1
    elif request_destination < curr_elev_location:
      # Start going down
      elevator_object.moving_status = -1
    elevator_object.save()

    # Destination reached, stop running
    # Open the door
    elevator_object.current_floor = request_destination
    elevator_object.moving_status = 0
    elevator_object.is_door_open = True
    elevator_object.save()

    elev_request.is_active = False
    elev_request.save()


def check_building(building : Building):
  '''
  Filter all the elevators running in an elevator system
  and process their requests one by one.
  '''
  elevators_running = Elevator.objects.filter(
    building = building,
    is_operational = True,
  )

  for elevator in elevators_running:
    move_elevator(elevator_object = elevator,building = building)


def final_run():
  '''
  Run the process for all elevator systems
  '''
  buildings = Building.objects.all().order_by('id')

  for building in buildings:
    check_building(building = building)