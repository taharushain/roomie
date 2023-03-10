# Generated by Django 4.1.2 on 2022-11-02 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_profile_department_profile_ip_phone"),
        ("booking", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="meeting",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="meetings",
                to="users.profile",
            ),
        ),
    ]
