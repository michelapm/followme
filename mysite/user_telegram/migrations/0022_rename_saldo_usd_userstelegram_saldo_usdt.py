# Generated by Django 4.0.4 on 2022-06-01 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_telegram', '0021_remove_userstelegram_saldo_ref_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userstelegram',
            old_name='saldo_usd',
            new_name='saldo_usdt',
        ),
    ]