# Generated by Django 5.1 on 2024-12-22 18:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("company", "0002_companys_com_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="companys",
            name="customer_id",
            field=models.CharField(default="customer_id", max_length=20),
        ),
        migrations.AddField(
            model_name="companys",
            name="customer_name",
            field=models.CharField(default="customer_name", max_length=50),
        ),
        migrations.AddField(
            model_name="companys",
            name="customer_passport_image",
            field=models.CharField(default="customer_image", max_length=100),
        ),
        migrations.AddField(
            model_name="companys",
            name="customer_passport_number",
            field=models.CharField(default="customer_passport_id", max_length=20),
        ),
        migrations.AddField(
            model_name="companys",
            name="customer_phone",
            field=models.CharField(default="customer_phone", max_length=20),
        ),
        migrations.AddField(
            model_name="companys",
            name="travel_id",
            field=models.CharField(default="id", max_length=20),
        ),
    ]
