# Generated by Django 4.0.4 on 2022-05-24 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_telegram', '0013_planes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacion',
            name='fecha_publicacion',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha de la publicacion'),
        ),
    ]
