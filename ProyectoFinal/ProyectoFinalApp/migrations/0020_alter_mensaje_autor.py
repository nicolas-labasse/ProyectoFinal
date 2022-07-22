# Generated by Django 4.0.5 on 2022-07-07 20:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ProyectoFinalApp', '0019_alter_mensaje_autor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensaje',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='autor', to=settings.AUTH_USER_MODEL),
        ),
    ]
