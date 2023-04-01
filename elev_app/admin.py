from django.contrib import admin


#model imports
from .models import *
# Register your models here.

admin.site.register(Building)
admin.site.register(Elevator)
admin.site.register(ElevatorRequest)