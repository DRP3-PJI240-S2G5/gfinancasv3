# Generated by Django 5.1.3 on 2024-11-22 21:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_responsabilidade"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Despesa",
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
                ("valor", models.DecimalField(decimal_places=2, max_digits=10)),
                ("justificativa", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Elemento",
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
                ("elemento", models.CharField(max_length=256)),
                ("descricao", models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name="TipoGasto",
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
                ("tipoGasto", models.CharField(max_length=256)),
                ("descricao", models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name="Verba",
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
                ("dataAtribuicao", models.DateTimeField(auto_now_add=True)),
                ("ano", models.IntegerField(verbose_name="Ano")),
                ("descricao", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameField(
            model_name="responsabilidade",
            old_name="IdDepartamento",
            new_name="departamento",
        ),
        migrations.RenameField(
            model_name="responsabilidade",
            old_name="Observacao",
            new_name="observacao",
        ),
        migrations.RenameField(
            model_name="responsabilidade",
            old_name="IdUser",
            new_name="user",
        ),
        migrations.RenameField(
            model_name="subordinacao",
            old_name="IdDepartamentoA",
            new_name="departamentoA",
        ),
        migrations.RenameField(
            model_name="subordinacao",
            old_name="IdDepartamentoB",
            new_name="departamentoB",
        ),
        migrations.RenameField(
            model_name="subordinacao",
            old_name="Observacao",
            new_name="observacao",
        ),
        migrations.AddConstraint(
            model_name="responsabilidade",
            constraint=models.UniqueConstraint(
                fields=("user", "departamento"),
                name="unique_user_departamento_responsabilidade",
            ),
        ),
        migrations.AddField(
            model_name="despesa",
            name="departamento",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="despesas_departamento",
                to="core.departamento",
            ),
        ),
        migrations.AddField(
            model_name="despesa",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="despesas",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="despesa",
            name="elemento",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="despesas_elemento",
                to="core.elemento",
            ),
        ),
        migrations.AddField(
            model_name="despesa",
            name="tipoGasto",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="despesas_tipoGasto",
                to="core.tipogasto",
            ),
        ),
        migrations.AddField(
            model_name="verba",
            name="departamento",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="verbas",
                to="core.departamento",
                verbose_name="verbas atribuidas",
            ),
        ),
        migrations.AddField(
            model_name="verba",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="verbas_estipuladas",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuário que atribuiu",
            ),
        ),
        migrations.AddConstraint(
            model_name="verba",
            constraint=models.UniqueConstraint(
                fields=("departamento", "ano"), name="unique_departamento_ano_verba"
            ),
        ),
    ]
