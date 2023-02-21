from django.db import models

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

class RackType(models.Model):
    rack_type_name = models.CharField(max_length=100)
    cell_x = models.IntegerField
    cell_y = models.IntegerField
    color = models.CharField(max_length=30)
    storage_time = models.IntegerField
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.rack_type_name

class ContainerType(models.Model):
    containet_type = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    rack_types = models.ManyToManyField(RackType)

    def __str__(self):
        return self.containet_type

class Workflow(models.Model):
    workflow = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    rack_types = models.ManyToManyField(RackType)

    def __str__(self):
        return self.workflow

class AcrhiveRacks(models.Model):
    rack_type_name = models.ForeignKey(RackType, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=25)

    def __str__(self):
        return self.rack_type_name

# class RealBase(models.Model):
#     sample_number = models.IntegerField
#     label_id = models.IntegerField
#     status = models.CharField(max_length=5)
#     received_by = models.CharField(max_length=50)
#     location = models.CharField(max_length=20)
#     template = models.CharField(max_length=20)
#     containet_type = models.CharField(max_length=30)
#     workflow = models.CharField(max_length=50)

#     def __str__(self):
#         return self.label_id

#     class Meta:
#         managed = False
#         db_table = ""





