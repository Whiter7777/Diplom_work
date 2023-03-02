from django.http import HttpResponse
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import Location, RackType, Status, ContainerType, Workflow, AcrhiveRacks, Archive, MainDbTable
from django.http import HttpResponseRedirect, HttpResponseNotFound
import datetime

# Create your views here.

def login_success(request):
    if request.user.groups.filter(name="Managment").exists():
        return redirect(create)
    elif request.user.groups.filter(name="Laboratory").exists():
        return redirect(archiving)
    elif request.user.groups.filter(name="Cleaning").exists():
        return redirect(cleaning)
    elif request.user.groups.filter(name="View").exists():
        return redirect(viewing)
    else:
        return redirect(main_archive)

def test_auth(request):
    return render(request, "auth.html")

def auth(request):
    login = request.POST.get("username", "Undefined")
    password = request.POST.get("password", "Undefined")
    return HttpResponse(f"<h2>Login: {login} Password: {password}</h2>")

def main_archive(request):
    return render(request, "base.html")


    
def cleaning(request):
    if request.user.groups.filter(name="Cleaning").exists():
        return render(request, "cleaning.html")
    else:
        return redirect(main_archive)

def viewing(request):
    if request.user.groups.filter(name="View").exists():
        return render(request, "viewing.html")
    else:
        return redirect(main_archive)

def manage(request):
    #if request.user.get_username() == "Manager":
    if request.user.groups.filter(name="Managment").exists():
        return render(request, "manage.html")
    else:
        return redirect(main_archive)

def index(request):
    if request.user.groups.filter(name="Managment").exists():
        if request.method == "POST":
            archive_rack = AcrhiveRacks()
            archive_rack.rack_type_name_id = request.POST.get("rack_type_name")
            archive_rack.close_data = datetime.datetime.now()
            archive_rack.save()
            return HttpResponseRedirect("/index")
        rack_types = RackType.objects.all()
        archive_racks = AcrhiveRacks.objects.all()
        return render(request, "index.html", {"rack_types": rack_types, "archive_racks": archive_racks})
    else:
        return redirect(main_archive)

def create(request):
    if request.user.groups.filter(name="Managment").exists():
        if request.method == "POST":
            rack_type = RackType()
            rack_type.rack_type_name = request.POST.get("rack_type_name")
            rack_type.cell_x = request.POST.get("cell_x")
            rack_type.cell_y = request.POST.get("cell_y")
            rack_type.color = request.POST.get("color")
            rack_type.storage_time = request.POST.get("storage_time")
            rack_type.location_id = request.POST.get("location")
            rack_type.status_id = request.POST.get("status")
            rack_type.description = request.POST.get("description")
            container_type_ids = request.POST.getlist("container_types")
            workflow_ids = request.POST.getlist("workflows")
            try:
                rack_type.save()
                container_types = ContainerType.objects.filter(id__in = container_type_ids)
                rack_type.container_types.set(container_types)
                workflows = Workflow.objects.filter(id__in = workflow_ids)
                rack_type.workflows.set(workflows)
                return HttpResponseRedirect("/index")
            except IntegrityError:
                return HttpResponse("ERROR: rack_type_name already exists!")
        locations = Location.objects.all()
        statuses = Status.objects.all()
        container_types = ContainerType.objects.all().order_by("container_type")
        workflows = Workflow.objects.all().order_by("workflow")
        return render(request, "create.html", {"locations": locations, "statuses": statuses, "container_types": container_types, "workflows": workflows})
    else:
        return redirect(main_archive)
    
def delete_rack_type(request, id):
    try:
        rack_type = RackType.objects.get(id=id)
        rack_type.delete()
        return HttpResponseRedirect("/index")
    except RackType.DoesNotExist:
            return HttpResponseNotFound("<h2>RackType not found</h2>")

def delete_archive_rack(request, id):
    try:
        archive_rack = AcrhiveRacks.objects.get(id=id)
        archive_rack.delete()
        return HttpResponseRedirect("/index")
    except RackType.DoesNotExist:
            return HttpResponseNotFound("<h2>RackType not found</h2>")


def archiving(request):
    if request.user.groups.filter(name="Laboratory").exists():
        archive_racks = AcrhiveRacks.objects.all()
        return render(request, "archiving.html", {"archive_racks": archive_racks})
    else:
        return redirect(main_archive)
    


def archivation(request):
    if request.method == "POST":
        archive_rack_id = request.POST.get("archive_rack_id", "Undefined")
        try:
            archive_racks = AcrhiveRacks.objects.get(id = archive_rack_id)
            if archive_racks.status == "Closed":
                return HttpResponse(f"""
                        <div>Данный штатив закрыт для архивации</div>
                    """)
            else:
                archive_rack = archive_racks.id
                rack_type_name = archive_racks.rack_type_name
                rack_type = RackType.objects.get(rack_type_name = rack_type_name)
                x = rack_type.cell_x
                y = rack_type.cell_y
                return HttpResponse(f"""
                            <div>Номер штатива: {archive_rack}</div>
                            <div>X: {x}</div>
                            <div>Y: {y}</div>
                        """)
        except AcrhiveRacks.DoesNotExist:
            return HttpResponseNotFound("<h2>AcrhiveRacks not found</h2>")

labels = MainDbTable.objects.using("main").all()
labels = labels.filter(label_id = "3302144845")
for i in labels:
    print(f"{i.location}, {i.containet_type}, {i.template}")


# def edit(request, id):
#     try:
#         rack_type = RackType.objects.get(id=id)
#         if request.method == "POST":
#             rack_type.rack_type_name = request.POST.get("rack_type_name")
#             rack_type.cell_x = request.POST.get("cell_x")
#             rack_type.cell_y = request.POST.get("cell_y")
#             rack_type.color = request.POST.get("color")
#             rack_type.storage_time = request.POST.get("storage_time")
#             rack_type.location_id = request.POST.get("location")
#             rack_type.status_id = request.POST.get("status")
#             rack_type.description = request.POST.get("description")
#             container_type_ids = request.POST.getlist("container_types")
#             workflow_ids = request.POST.getlist("workflows")
#             rack_type.save()
#             container_types = ContainerType.objects.filter(id__in = container_type_ids)
#             rack_type.container_types.set(container_types)
#             workflows = Workflow.objects.filter(id__in = workflow_ids)
#             rack_type.workflows.set(workflows)
#             return HttpResponseRedirect("/index")
#         else:
#             locations = Location.objects.all()
#             statuses = Status.objects.all()
#             container_types = ContainerType.objects.all()
#             workflows = Workflow.objects.all()
#             return render(request, "create.html", {"locations": locations, "statuses": statuses, "container_types": container_types, "workflows": workflows})
#     except RackType.DoesNotExist:
#         return HttpResponseNotFound("<h2>RackType not found</h2>")
    



# from django.db import connection

# with open("E:\Diplom_work\CONTAINER_TYPE.csv", "r") as inf:
#     for line in inf:
#         line = (line.strip().split(";"))

#         reviewers_records = [(line[0], "Null")]
#         insert_archiv_table_query = """
#             INSERT INTO archive_app_containertype (container_type, description)
#             VALUES ( %s, %s )
#         """
#         with connection.cursor() as cursor:
#             cursor.executemany(insert_archiv_table_query, reviewers_records)

# with open("E:\Diplom_work\LOCATION.csv", "r") as inf:
#     for line in inf:
#         line = (line.strip().split(";"))

#         reviewers_records = [(line[0], "Null")]
#         insert_archiv_table_query = """
#             INSERT INTO archive_app_location (location, description)
#             VALUES ( %s, %s )
#         """
#         with connection.cursor() as cursor:
#             cursor.executemany(insert_archiv_table_query, reviewers_records)

# with open("E:\Diplom_work\STATUS.csv", "r") as inf:
#     for line in inf:
#         line = (line.strip().split(";"))

#         reviewers_records = [(line[0], line[1])]
#         insert_archiv_table_query = """
#             INSERT INTO archive_app_status (status, description)
#             VALUES ( %s, %s )
#         """
#         with connection.cursor() as cursor:
#             cursor.executemany(insert_archiv_table_query, reviewers_records)

# with open("E:\Diplom_work\X_WORKFLOW.csv", "r") as inf:
#     for line in inf:
#         line = (line.strip().split(";"))

#         reviewers_records = [(line[0], "Null")]
#         insert_archiv_table_query = """
#             INSERT INTO archive_app_workflow (workflow, description)
#             VALUES ( %s, %s )
#         """
#         with connection.cursor() as cursor:
#             cursor.executemany(insert_archiv_table_query, reviewers_records)


