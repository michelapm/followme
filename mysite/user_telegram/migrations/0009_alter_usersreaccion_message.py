# Generated by Django 4.0.4 on 2022-05-22 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_telegram', '0008_alter_usersmetodospagos_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersreaccion',
            name='message',
            field=models.CharField(max_length=200, verbose_name='Publicacion id'),
        ),
    ]