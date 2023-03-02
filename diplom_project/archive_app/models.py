from django.db import models
from colorfield.fields import ColorField
from datetime import date

class Status(models.Model):
    status = models.CharField(max_length=10)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.status

class Location(models.Model):
    location = models.CharField(max_length=20)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.location

class ContainerType(models.Model):
    container_type = models.CharField(max_length=30)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.container_type

class Workflow(models.Model):
    workflow = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.workflow

class RackType(models.Model):
    rack_type_name = models.CharField(max_length=100, unique=True)
    cell_x = models.PositiveSmallIntegerField()
    cell_y = models.PositiveSmallIntegerField()
    # color = models.CharField(max_length=30)
    color = ColorField(default='#FF0000')
    storage_time = models.PositiveIntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    container_types = models.ManyToManyField(ContainerType, through="RackType_ContainerType")
    workflows = models.ManyToManyField(Workflow, through="RackType_Workflow")
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.rack_type_name

class RackType_ContainerType(models.Model):
    rack_type_name = models.ForeignKey(RackType, on_delete=models.CASCADE)
    container_type = models.ForeignKey(ContainerType, on_delete=models.CASCADE)


class RackType_Workflow(models.Model):
    rack_type_name = models.ForeignKey(RackType, on_delete=models.CASCADE)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    

class AcrhiveRacks(models.Model):
    rack_type_name = models.ForeignKey(RackType, on_delete=models.CASCADE)
    close_data = models.DateTimeField()
    barcode = models.CharField(max_length=25)
    status = models.CharField(max_length=10, default="Open")

    def __str__(self):
        return str(self.rack_type_name)

class Archive(models.Model):
    archive_rack = models.ForeignKey(AcrhiveRacks,on_delete=models.CASCADE)
    archiving_number = models.CharField(max_length=20)
    coord_x = models.PositiveSmallIntegerField()
    coord_y = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.archiving_number)


class MainDbTable(models.Model):
    sample_number = models.CharField(max_length=10, blank=True, null=True)
    label_id = models.CharField(max_length=20, blank=True, null=True)
    x_status = models.CharField(max_length=10, blank=True, null=True)
    received_by = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=20, blank=True, null=True)
    template = models.CharField(max_length=20, blank=True, null=True)
    containet_type = models.CharField(max_length=30, blank=True, null=True)
    x_workflow = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'main_db_table'


