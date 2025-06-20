# Generated by Django 5.1 on 2024-12-18 13:48

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Companys",
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
                ("com_api", models.TextField()),
                ("com_end_travel", models.CharField(max_length=100)),
                ("com_end_add_booking", models.CharField(max_length=100)),
                ("travel_from", models.CharField(max_length=50)),
                ("travel_to", models.CharField(max_length=50)),
                ("travel_price", models.CharField(max_length=50)),
                ("travel_num_seats", models.CharField(max_length=50)),
                ("travel_start_time", models.CharField(max_length=50)),
                ("travel_wait_time", models.CharField(max_length=50)),
            ],
        ),
    ]
