from django.contrib import admin
from .models import Status, Location, RackType, ContainerType, Workflow, RackType_ContainerType, RackType_Workflow, AcrhiveRacks, Archive

admin.site.register(Status)
admin.site.register(Location)
admin.site.register(ContainerType)
admin.site.register(Workflow)
admin.site.register(RackType)
admin.site.register(RackType_ContainerType)
admin.site.register(RackType_Workflow)
admin.site.register(AcrhiveRacks)
admin.site.register(Archive)

