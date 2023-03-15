from django.http import HttpResponse
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import Location, RackType, Status, ContainerType, Workflow, AcrhiveRacks, Archive, MainDbTable
from django.http import HttpResponseRedirect, HttpResponseNotFound
import datetime
from datetime import timedelta
from .forms import UserForm, FindSample
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


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

# def test_auth(request):
#     return render(request, "auth.html")

# def auth(request):
#     login = request.POST.get("username", "Undefined")
#     password = request.POST.get("password", "Undefined")
#     return HttpResponse(f"<h2>Login: {login} Password: {password}</h2>")

def main_archive(request):
    return render(request, "base.html")

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
            archive_rack.reset_date = datetime.datetime.now()
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
                messages.error(request, 'Тип штатива с таким именем уже существует')
                # return HttpResponse("ERROR: rack_type_name already exists!")
            except ValueError:
                messages.error(request, 'Поля Cell X, Cell Y и Storage time должны быть заполнены')
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
                messages.error(request, 'Данный штатив закрыт для архивации')
                return HttpResponseRedirect("/archiving")
                # return HttpResponse(f"""
                #         <div>Данный штатив закрыт для архивации</div>
                #     """)
            elif archive_racks.status == "Open" and AcrhiveRacks.objects.filter(status="In work").exists():
                messages.error(request, 'Сначала необходимо закрыть штативы со статусом "In Work"')
                return HttpResponseRedirect("/archiving")
                # return HttpResponse(f"""
                #         <div><h3>Есть незакрытые штативы в работе</h3></div>
                #     """)
            else:
                with open("number.txt", "w") as file:
                    file.write(str(archive_rack_id))
                # archive_rack = archive_racks.id
                # rack_type_name = archive_racks.rack_type_name
                # rack_type = RackType.objects.get(rack_type_name = rack_type_name)
                # x = rack_type.cell_x
                # y = rack_type.cell_y
                return HttpResponseRedirect("/archiv_main")
                # return HttpResponse(f"""
                #             <div>Номер штатива: {archive_rack}</div>
                #             <div>X: {x}</div>
                #             <div>Y: {y}</div>
                #         """)
        except AcrhiveRacks.DoesNotExist:
            messages.error(request, 'Такого штатива не существует')
            return HttpResponseRedirect("/archiving")
            # return HttpResponseNotFound("<h2>AcrhiveRacks not found</h2>")
        except ValueError:
            messages.error(request, 'Введено некорректное значение')
            return HttpResponseRedirect("/archiving")

        

def archiv_main(request):
    if request.user.groups.filter(name="Laboratory").exists():
        with open("number.txt", "r") as file:
            archive_rack_id = int(file.read())
        archive_racks = AcrhiveRacks.objects.get(id = archive_rack_id)
        archive_rack = archive_racks.id
        # print(archive_rack)
        rack_status = archive_racks.status
        # print(rack_status)
        # print(archive_rack)
        rack_type_name = archive_racks.rack_type_name
        # print(rack_type_name)
        rack_type = RackType.objects.get(rack_type_name = rack_type_name)
        x = rack_type.cell_x
        # print(x)
        y = rack_type.cell_y
        # print(y)
        archive_location = rack_type.location.location
        archive_container_types = rack_type.container_types
        lst_container_types = []
        lst_workflows = []
        for i in archive_container_types.all():
            lst_container_types.append(i.container_type)
        archive_status = rack_type.status.status
        archive_workflows = rack_type.workflows
        for i in archive_workflows.all():
            lst_workflows.append(i.workflow)
        # print(archive_location)
        # print(archive_status)
        # print(lst_container_types)
        # print(lst_workflows)
        lst_x = [i for i in range(x)]
        lst_y = [i for i in range(y)]

        try:
            latest_archiv = Archive.objects.latest("id")
            rack_in_work = AcrhiveRacks.objects.filter(id = archive_rack_id).update(status="In work")
            
            if latest_archiv.archive_rack.id != archive_rack:
                status = [["Empty" for j in lst_x] for i in lst_y]
                coord_x = 1
                coord_y = 1
            else:
                x_fact = latest_archiv.coord_x
                y_fact = latest_archiv.coord_y
                status = [["Empty" for j in lst_x] for i in lst_y]

                for i in range(len(status)):
                    for j in range(len(status[i])):
                        status[i][j] = "Full"
                        if i == y_fact-1 and j == x_fact-1:
                            break
                    if i == y_fact-1 and j == x_fact-1:
                        break

                if x_fact + 1 > x:
                    if y_fact + 1 > y:
                        rack_closed = AcrhiveRacks.objects.filter(id = archive_rack_id).update(status="Closed")
                        date_closed = AcrhiveRacks.objects.filter(id = archive_rack_id).update(reset_date=datetime.datetime.now())
                        return HttpResponseRedirect("/rack_closed")
                    #     return HttpResponse(f"""
                    #     <div>Данный штатив закрыт для архивации</div>
                    # """)
                    else:
                        coord_x = 1
                        coord_y = y_fact + 1
                else:
                    coord_x = x_fact + 1
                    coord_y = y_fact

        except Archive.DoesNotExist:
            status = [["Empty" for j in lst_x] for i in lst_y]
            coord_x = 1
            coord_y = 1

        if request.method == "POST":
            archive = Archive()
            archive.archive_rack = archive_racks
            archive.archiving_number = request.POST.get("archiving_number")
            a = request.POST.get("archiving_number")
            archive.coord_x = coord_x
            archive.coord_y = coord_y
            
            labels = MainDbTable.objects.using("main").all()
            labels = labels.filter(sample_number = request.POST.get("archiving_number"))
            for i in labels:
                main_location = i.location
                main_container_type = i.containet_type
                main_status = i.x_status
                main_workflow = i.x_workflow
                # print(main_location == archive_location)
                # print(main_status == archive_status)
                # print(main_container_type in lst_container_types)
                # print(main_workflow in lst_workflows)
            try:
                b =  Archive.objects.filter(archiving_number = a).exists()
                if b:
                    messages.error(request, 'Проба с таким номером уже заархивирована')
                elif main_location == archive_location and main_status == archive_status and main_container_type in lst_container_types and main_workflow in lst_workflows:
                    archive.save()
                    return HttpResponseRedirect("/archiv_main")
                else:
                    messages.error(request, 'Параметры пробы не соответствуют параметрам типа архивного штатива')
                    # return HttpResponseRedirect("/archiv_main")
                    # return HttpResponse(f"""
                    #         <div>Параметры пробы не соответствуют параметрам типа архивного штатива</div>
                    #     """)
            except:
                    messages.error(request, 'Такого номера не существует')
                    # return HttpResponseRedirect("/archiv_main")
                # return HttpResponse(f"""
                #             <div>Данного номера не существует</div>
                #         """)
        
        # for i in range(len(status)):
        #     for j in range(len(status[i])):
        #         status[coord_y-1][coord_x-1] = "Full"

        return render(request, "archive_main.html", {
            "archive_rack": archive_rack,
            "x": x, 
            "y": y,
            "lst_x": lst_x,
            "lst_y": lst_y,
            "status": status
        })
    else:
        return redirect(main_archive)


def rack_closed(request):
    return render(request, "rack_closed.html")


def cleaning(request):
    if request.user.groups.filter(name="Cleaning").exists():
        data_now = datetime.datetime.now()
        archive_racks = AcrhiveRacks.objects.filter(status = "Closed")
        for archive_rack in archive_racks:
            time = archive_rack.rack_type_name.storage_time
            if (archive_rack.reset_date + datetime.timedelta(hours=time)).strftime("%d.%m.%Y %H:%M:%S") < data_now.strftime("%d.%m.%Y %H:%M:%S"):
                reset = AcrhiveRacks.objects.filter(id = archive_rack.id).update(barcode="Ready to reset")
            else:
                reset = AcrhiveRacks.objects.filter(id = archive_rack.id).update(barcode="Not ready to reset")
        return render(request, "cleaning.html", {"archive_racks": archive_racks, "data_now": data_now})
    else:
        return redirect(main_archive)


def delete_archive(request, id):
    try:
        archives = Archive.objects.filter(archive_rack = id)
        for i in archives:
            i.delete()
        rack_closed = AcrhiveRacks.objects.filter(id = id).update(status="Open")
        return HttpResponseRedirect("/cleaning")
    except RackType.DoesNotExist:
            return HttpResponseNotFound("<h2>Archive not found</h2>")


def viewing(request):
    if request.user.groups.filter(name="View").exists():
        submitbutton= request.POST.get("submit")
        find_sample = ""
        report = ""
        id = ""
        x = ""
        y = ""
        color = ""
        form = FindSample(request.POST or None)
        try:
            if form.is_valid():
                find_sample = str(form.cleaned_data.get("find_sample"))
                sample_number = Archive.objects.get(archiving_number = find_sample)
                report = "Номер найден"
                id = sample_number.archive_rack.id
                x = sample_number.coord_x
                y = sample_number.coord_y
                color = sample_number.archive_rack.rack_type_name.color
            context= {"color": color, "report":report, "id": id, "x": x, "y": y, 'form': form, 'find_sample': find_sample,'submitbutton': submitbutton}
            return render(request, "viewing.html", context)
        except:
            messages.error(request, 'Номер не найден')
            return HttpResponseRedirect("/viewing")
            # report = "Sample not found"
            # context= {"report":report, 'form': form, 'submitbutton': submitbutton}
            # return render(request, "viewing.html", context)
    else:
        return redirect(main_archive)


# def viewing(request):
#     if request.user.groups.filter(name="View").exists():
#         submitbutton= request.POST.get("submit")
#         find_sample = ""
#         report = ""
#         id = ""
#         x = ""
#         y = ""
#         form = FindSample(request.POST or None)
#         if form.is_valid():
#             find_sample = str(form.cleaned_data.get("find_sample"))
#             sample_number = Archive.objects.get(archiving_number = find_sample)
#             report = "Sample found"
#             id = sample_number.archive_rack.id
#             x = sample_number.coord_x
#             y = sample_number.coord_y
#         context= {"report":report, "id": id, "x": x, "y": y, 'form': form, 'find_sample': find_sample,'submitbutton': submitbutton}
#         return render(request, "viewing.html", context)
#     else:
#         return redirect(main_archive)




# labels = MainDbTable.objects.using("main").all()
# labels = labels.filter(sample_number = "246344068")
# for i in labels:
#     main_location = i.location
#     main_container_type = i.containet_type
#     main_status = i.x_status
#     main_workflow = i.x_workflow
# print(main_location, main_container_type, main_status, main_workflow)

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


