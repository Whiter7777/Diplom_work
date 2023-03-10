# Generated by Django 4.1.6 on 2023-03-05 13:19

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AcrhiveRacks",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("close_data", models.DateTimeField()),
                ("reset_date", models.DateTimeField()),
                ("barcode", models.CharField(max_length=25)),
                ("status", models.CharField(default="Open", max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="ContainerType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("container_type", models.CharField(max_length=30)),
                ("description", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("location", models.CharField(max_length=20)),
                ("description", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="RackType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rack_type_name", models.CharField(max_length=100, unique=True)),
                ("cell_x", models.PositiveSmallIntegerField()),
                ("cell_y", models.PositiveSmallIntegerField()),
                (
                    "color",
                    colorfield.fields.ColorField(
                        default="#FF0000", image_field=None, max_length=18, samples=None
                    ),
                ),
                ("storage_time", models.PositiveIntegerField()),
                ("description", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Status",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.CharField(max_length=10)),
                ("description", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Workflow",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("workflow", models.CharField(max_length=50)),
                ("description", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="RackType_Workflow",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "rack_type_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="archive_app.racktype",
                    ),
                ),
                (
                    "workflow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="archive_app.workflow",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RackType_ContainerType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "container_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="archive_app.containertype",
                    ),
                ),
                (
                    "rack_type_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="archive_app.racktype",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="racktype",
            name="container_types",
            field=models.ManyToManyField(
                through="archive_app.RackType_ContainerType",
                to="archive_app.containertype",
            ),
        ),
        migrations.AddField(
            model_name="racktype",
            name="location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="archive_app.location"
            ),
        ),
        migrations.AddField(
            model_name="racktype",
            name="status",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="archive_app.status"
            ),
        ),
        migrations.AddField(
            model_name="racktype",
            name="workflows",
            field=models.ManyToManyField(
                through="archive_app.RackType_Workflow", to="archive_app.workflow"
            ),
        ),
        migrations.CreateModel(
            name="Archive",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("archiving_number", models.CharField(max_length=20)),
                ("coord_x", models.PositiveSmallIntegerField()),
                ("coord_y", models.PositiveSmallIntegerField()),
                (
                    "archive_rack",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="archive_app.acrhiveracks",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="acrhiveracks",
            name="rack_type_name",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="archive_app.racktype"
            ),
        ),
    ]
