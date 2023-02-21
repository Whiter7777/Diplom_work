from django.contrib import admin

from django.contrib import admin
from .models import Status, Location, RackType, ContainerType, Workflow, AcrhiveRacks

# Register your models here.
admin.site.register(Status)
admin.site.register(Location)
admin.site.register(RackType)
admin.site.register(ContainerType)
admin.site.register(Workflow)
admin.site.register(AcrhiveRacks)
# Register your models here.
