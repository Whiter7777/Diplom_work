from django.urls import path, re_path
from archive_app import views

urlpatterns = [
    re_path(r'login_success/$', views.login_success, name='login_success'),
    # path("auth/", views.test_auth),
    # path("auth/user/", views.auth),
    path("", views.main_archive),
    path("index/", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("manage/", views.manage),
    path("archiving/", views.archiving, name="archiving"),
    path("archiving/archivation/", views.archivation),
    path("cleaning/", views.cleaning),
    path("viewing/", views.viewing),
    path("index/delete_rack_type/<int:id>/", views.delete_rack_type),
    path("index/delete_archive_rack/<int:id>/", views.delete_archive_rack),
    path("cleaning/delete_archive/<int:id>", views.delete_archive),
    # path("test_1/", views.test),
    path("archiv_main/", views.archiv_main),
    path("rack_closed/", views.rack_closed),
]
