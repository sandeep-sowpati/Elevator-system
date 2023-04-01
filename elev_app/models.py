from django.db import models
from django.db.models.signals import post_save

from django.dispatch import receiver


from django.core.exceptions import ValidationError


# Create your models here.


class Building(models.Model):
    '''
    Bullding Model => which represents the Building with multiple elevators(Elevator System)
    '''
    name = models.CharField(max_length=30)
    max_floor = models.IntegerField()
    number_of_elevators =  models.IntegerField(default=1)

    #string representation of the Building model
    def __str__(self) -> str:
        elev_return = 'Building {name}'
        return elev_return.format(name = self.name)

class Elevator(models.Model):
    '''
    Elevator Model => which represents single lift and the properties.
    '''

    class ElevatorStatus(models.IntegerChoices):
        #Django enum or choices field to identify whether to identify the elevator is on hold, or moving.
        IDLE = 0
        MOVING_UP = 1
        MOVING_DOWN = -1

    # in a building multiple elevators are going to be there to identify which system this elevator belongs to
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='elevators')
    elevator_number = models.IntegerField()
    is_operational = models.BooleanField(default=True)

    # by default the elevator is going to be on 0 th floor.
    current_floor = models.IntegerField(default=0)
    # by default the door of the elevator is closed
    is_door_open = models.BooleanField(default=False)
    moving_status = models.IntegerField(choices=ElevatorStatus.choices, default=0)

    # string representation of the Elevator model
    def __str__(self):
        build = self.building.name
        return f"{build} : Elevator {self.elevator_number}"


@receiver(post_save, sender=Building)
def create_elevators(sender, instance, created, **kwargs):
    '''
    Django Signal to initialise the the Elevators , Whenever a Building is created django will will trigger this signal
    and this signal craters the specified number of Elevators
    '''
    if created:
        for i in range(instance.number_of_elevators):
            Elevator.objects.create(building=instance, elevator_number=i+1)


class ElevatorRequest(models.Model):
    '''
    Model fo Elevator and to get the details of the particular adapter.
    '''
    elevator = models.ForeignKey(Elevator,on_delete=models.CASCADE)

    requested_floor   = models.IntegerField()
    #added
    destination_floor = models.IntegerField()

    request_time = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.elevator} is moving towards {self.destination_floor}'

    def clean(self):
        errors = {}
        if self.destination_floor < 0:
            errors['destination_floor'] = 'The Destiantion must be more than 0.'

        elif self.destination_floor > self.elevator.building.max_floor:
            errors['destination_floor']  = f'The Destiantion must be less than {self.elevator.building.max_floor}.'

        elif self.requested_floor== self.destination_floor:
            errors['destination_floor'] = 'Requested Floor and the Destiantion Floor cant be the same'

        if errors:
            raise ValidationError(errors)
