# Generated by Django 2.0.2 on 2018-03-20 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0018_auto_20180313_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_group_membership',
            name='share_admin',
            field=models.BooleanField(default=True, help_text='Designates whether this user can add or remove shares from this group.', verbose_name='Share admin'),
        ),
        migrations.AlterField(
            model_name='user_group_membership',
            name='group_admin',
            field=models.BooleanField(default=False, help_text='Designates whether this user can invite other users to this group, and adjust other user rights.', verbose_name='Group admin'),
        ),
    ]
