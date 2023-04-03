from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Building, Elevator, ElevatorRequest
from .serializers import BuildingSerializer, ElevatorSerializer, ElevatorRequestSerializer


class BuildingCreateView(generics.ListCreateAPIView):
    '''
    Create a new building and initialize n elevators in the building.
    '''
    serializer_class = BuildingSerializer
    queryset = Building.objects.all()


class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    @action(detail=True, methods=['get'])
    def requests(self, request, pk=None):
        elevator = get_object_or_404(self.queryset, pk=pk)
        serializer = ElevatorRequestSerializer(elevator.requests.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def next_floor(self, request, pk=None):
        elevator_object = get_object_or_404(self.queryset, pk=pk)
        requests_pending = ElevatorRequest.objects.filter(
        elevator = elevator_object,
        is_active = True,
        ).order_by('request_time').first()

        # return_dict = {

        # }

        if requests_pending is None:
            return_dict = {
                'running' : False,
                'details' : 'The Elevator doesnt have any pending requests'
            }

        elif not elevator_object.is_operational:
            return_dict = {
                'running' : False,
                'details' : 'The Elevator is not operational'
            }
        elif requests_pending.requested_floor == elevator_object.current_floor:
            return_dict = {
                'running' : True,
                'details' : str(requests_pending.destination_floor)
            }
        else:
            return_dict = {
                'running' : True,
                'details' : str(requests_pending.requested_floor)
            }
        return Response(return_dict)

    @action(detail=True, methods=['get'])
    def moving_direction(self, request, pk=None):
        elevator = get_object_or_404(self.queryset, pk=pk)
        direction = elevator.moving_status
        direct = 'IDLE'
        if direction==-1:
            direct = 'DOWN'
        elif direction == 1:
            direct = 'UP'
        return Response({'direction': direct})

    @action(detail=True, methods=['post'])
    def request_elevator(self, request, pk=None):
        elevator = get_object_or_404(self.queryset, pk=pk)
        serializer = ElevatorRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(elevator=elevator)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['put'])
    def mark_not_working(self, request, pk=None):
        elevator = get_object_or_404(self.queryset, pk=pk)
        elevator.is_operational = False
        elevator.save()
        return Response({'message': 'Elevator marked as not working.'})

    @action(detail=True, methods=['put'])
    def mark_working(self, request, pk=None):
        elevator = get_object_or_404(self.queryset, pk=pk)
        elevator.is_operational = True
        elevator.save()
        return Response({'message': 'Elevator marked as working.'})

    @action(detail=True, methods=['put'])
    def open_door(self, request, pk=None):
        elevator = get_object_or_404(self.queryset, pk=pk)
        elevator.is_door_open = True
        return Response({'message': 'Door opened.'})

    @action(detail=True, methods=['put'])
    def close_door(self, request, pk=None):
        elevator = get_object_or_404(self.queryset, pk=pk)
        elevator.is_door_open = False
        return Response({'message': 'Door closed.'})