# Generated by Django 3.2 on 2021-05-04 14:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscriptions', '0004_auto_20210504_1308'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reader',
            new_name='Account',
        ),
    ]