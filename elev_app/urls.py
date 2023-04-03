from django.urls import path, include
from rest_framework import routers
from .views import *

#api-documentation
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

router = routers.DefaultRouter()
router.register('elevators', ElevatorViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('buildings/', BuildingCreateView.as_view(),name='building'),
    path('schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),
    path('elevators/<int:pk>/requests/', ElevatorViewSet.as_view({'get': 'requests'})),
    path('elevators/<int:pk>/next_floor/', ElevatorViewSet.as_view({'get': 'next_floor'})),
    path('elevators/<int:pk>/moving_direction/', ElevatorViewSet.as_view({'get': 'moving_direction'})),
    path('elevators/<int:pk>/request_elevator/', ElevatorViewSet.as_view({'post': 'request_elevator'})),
    path('elevators/<int:pk>/mark_not_working/', ElevatorViewSet.as_view({'put': 'mark_not_working'})),
    path('elevators/<int:pk>/mark_working/', ElevatorViewSet.as_view({'put': 'mark_working'})),
    path('elevators/<int:pk>/door/open/', ElevatorViewSet.as_view({'put': 'open_door'})),
    path('elevators/<int:pk>/door/close/', ElevatorViewSet.as_view({'put': 'close_door'})),
]