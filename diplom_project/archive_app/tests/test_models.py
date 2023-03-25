from django.test import TestCase
from archive_app.models import Location, RackType, Status, ContainerType, Workflow, AcrhiveRacks, Archive

class LocationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Location.objects.create(location = "Test", description = "Test")

    def test_location_label(self):
        location=Location.objects.get(id=1)
        field_label = location._meta.get_field("location").verbose_name
        self.assertEquals(field_label, "location")

    def test_description_label(self):
        description=Location.objects.get(id=1)
        field_label = description._meta.get_field("description").verbose_name
        self.assertEquals(field_label, "description")

    def test_location_max_length(self):
        location=Location.objects.get(id=1)
        max_length = location._meta.get_field("location").max_length
        self.assertEquals(max_length, 20)

    def test_description_max_length(self):
        description=Location.objects.get(id=1)
        max_length = description._meta.get_field("description").max_length
        self.assertEquals(max_length, 50)


# class RackTypeModelTest(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         RackType.objects.create(rack_type_name = "Test", cell_x = "2", cell_y = "3", 
#                                 color = '#FF0000', storage_time = "24")

