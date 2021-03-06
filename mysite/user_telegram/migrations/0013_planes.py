# Generated by Django 4.0.4 on 2022-05-24 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_telegram', '0012_alter_publicacion_options_alter_publicacion_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Planes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('fecha_modificacion', models.DateField(auto_now=True, verbose_name='Fecha de Modificación')),
                ('fecha_eliminacion', models.DateField(auto_now=True, verbose_name='Fecha de Eliminación')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre del Plan')),
                ('descriptcion', models.TextField(verbose_name='Descripccion del plan')),
                ('precio', models.FloatField(verbose_name='Precio del plan')),
                ('horas_republicacion', models.IntegerField(verbose_name='Cantidad de horas para poder publicar de nuevo')),
                ('automatic', models.BooleanField(default=True, verbose_name='Estado de republicacion automatico')),
            ],
            options={
                'verbose_name': 'Plan',
                'verbose_name_plural': 'Planes',
                'ordering': ['id'],
            },
        ),
    ]
