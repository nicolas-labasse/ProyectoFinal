# Generated by Django 4.0.5 on 2022-07-04 01:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoFinalApp', '0012_alter_mensaje_usuario_alter_mensaje_usuario_receptor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mensaje',
            name='usuario',
        ),
    ]
