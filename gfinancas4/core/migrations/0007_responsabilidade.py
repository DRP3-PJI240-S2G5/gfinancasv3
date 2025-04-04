# Generated by Django 4.2.16 on 2024-11-22 00:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0006_subordinacao"),
    ]

    operations = [
        migrations.CreateModel(
            name="Responsabilidade",
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
                ("dataCriacao", models.DateTimeField(auto_now_add=True)),
                ("Observacao", models.TextField(blank=True, null=True)),
                (
                    "IdDepartamento",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="responsaveis",
                        to="core.departamento",
                    ),
                ),
                (
                    "IdUser",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="responsabilidades",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
