# Generated by Django 2.2.24 on 2021-10-28 19:23

from django.db import migrations
import src.accounts.services.base_auth


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', src.accounts.services.base_auth.MyManager()),
            ],
        ),
    ]