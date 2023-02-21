from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Location, RackType, Status
from django.http import HttpResponseRedirect, HttpResponseNotFound

# Create your views here.
def test_auth(request):
    return render(request, "auth.html")

def auth(request):
    login = request.POST.get("username", "Undefined")
    password = request.POST.get("password", "Undefined")
    return HttpResponse(f"<h2>Login: {login} Password: {password}</h2>")

def main_archive(request):
    return render(request, "base.html")

def manage(request):
    #if request.user.get_username() == "Manager":
    if request.user.groups.filter(name="Managment").exists():
        return render(request, "manage.html")
    else:
        return redirect(main_archive)

def archiving(request):
    if request.user.groups.filter(name="Laboratory").exists():
        return render(request, "archiving.html")
    else:
        return redirect(main_archive)
    
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
    
def login_success(request):
    if request.user.groups.filter(name="Managment").exists():
        return redirect(manage)
    elif request.user.groups.filter(name="Laboratory").exists():
        return redirect(archiving)
    elif request.user.groups.filter(name="Cleaning").exists():
        return redirect(cleaning)
    elif request.user.groups.filter(name="View").exists():
        return redirect(viewing)
    else:
        return redirect(main_archive)

def index(request):
    rack_types = RackType.objects.all()
    return render(request, "index.html", {"rack_types": rack_types})
    

def create(request):
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
        rack_type.save()
        return HttpResponseRedirect("/index")
    locations = Location.objects.all()
    statuses = Status.objects.all()
    return render(request, "create.html", {"locations": locations, "statuses": statuses})

































# from django.db import connection

# with open("E:\Diplom_work\CONTAINER_TYPE.csv", "r") as inf:
#     for line in inf:
#         line = (line.strip().split(";"))

#         reviewers_records = [(line[0], "Null")]
#         insert_archiv_table_query = """
#             INSERT INTO archive_app_containertype (containet_type, description)
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