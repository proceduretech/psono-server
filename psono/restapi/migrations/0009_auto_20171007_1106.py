# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-07 11:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0008_token_valid_till'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group_Share_Right',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(help_text='The (public or secret) encrypted key with which the share is encrypted.', max_length=256, verbose_name='Key')),
                ('key_nonce', models.CharField(max_length=64, verbose_name='Key nonce')),
                ('title', models.CharField(help_text='The public (yet encrypted) title of the share right.', max_length=512, null=True, verbose_name='Title')),
                ('title_nonce', models.CharField(max_length=64, null=True, verbose_name='Title nonce')),
                ('type', models.CharField(help_text='The public (yet encrypted) type of the share right.', max_length=512, null=True, verbose_name='Type')),
                ('type_nonce', models.CharField(max_length=64, null=True, verbose_name='Type nonce')),
                ('read', models.BooleanField(default=True, help_text='Designates whether this user has "read" rights and can read this share', verbose_name='Read right')),
                ('write', models.BooleanField(default=False, help_text='Designates whether this user has "write" rights and can update this share', verbose_name='Write right')),
                ('grant', models.BooleanField(default=False, help_text='Designates whether this user has "grant" rights and can re-share this share', verbose_name='Grant right')),
                ('creator', models.ForeignKey(help_text='The user who created this share right', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='own_group_share_rights', to='restapi.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User_Group_Membership',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('secret_key', models.CharField(help_text='The secret key encrypted with the (public or secret) key of the user.', max_length=256, verbose_name='Secret Key')),
                ('secret_key_nonce', models.CharField(max_length=64, verbose_name='Key nonce')),
                ('secret_key_type', models.CharField(default=b'asymmetric', help_text='Key type of the secret key, either "symmetric", or "asymmetric"', max_length=16, verbose_name='Key type')),
                ('private_key', models.CharField(help_text='The Private Key encrypted with the (public or secret) key of the user.', max_length=256, verbose_name='Private key')),
                ('private_key_nonce', models.CharField(max_length=64, verbose_name='Private Key nonce')),
                ('private_key_type', models.CharField(default=b'asymmetric', help_text='Key type of the private key, either "symmetric", or "asymmetric"', max_length=16, verbose_name='Private Key type')),
                ('group_admin', models.BooleanField(default=False, help_text='Designates whether this user can invite other users to this group, and adjust other user rights', verbose_name='Group admin')),
                ('accepted', models.NullBooleanField(default=None, help_text='Defines if the share has been accepted, declined, or still waits for approval', verbose_name='Accepted')),
                ('creator', models.ForeignKey(help_text='The user who created this share right', null=True, on_delete=django.db.models.deletion.SET_NULL, to='restapi.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='group_user_right',
            name='group',
        ),
        migrations.RemoveField(
            model_name='group_user_right',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='group_user_right',
            name='user',
        ),
        migrations.RemoveField(
            model_name='group',
            name='shares',
        ),
        migrations.RemoveField(
            model_name='group',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user_share_right',
            name='owner',
        ),
        migrations.AddField(
            model_name='group',
            name='public_key',
            field=models.CharField(default='', max_length=256, verbose_name='public key'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user_share_right',
            name='creator',
            field=models.ForeignKey(help_text='The user who created this share right', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='own_user_share_rights', to='restapi.User'),
        ),
        migrations.AlterField(
            model_name='secret',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='secrets', to='restapi.User'),
        ),
        migrations.AlterField(
            model_name='share',
            name='user',
            field=models.ForeignKey(help_text='The share user is always the same as the group user, so the group user always keeps full control.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shares', to='restapi.User'),
        ),
        migrations.AlterField(
            model_name='user_share_right',
            name='user',
            field=models.ForeignKey(help_text='The user who will receive this share right', on_delete=django.db.models.deletion.CASCADE, related_name='foreign_user_share_rights', to='restapi.User'),
        ),
        migrations.DeleteModel(
            name='Group_User_Right',
        ),
        migrations.AddField(
            model_name='user_group_membership',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='restapi.Group'),
        ),
        migrations.AddField(
            model_name='user_group_membership',
            name='user',
            field=models.ForeignKey(help_text='The user who will receive this share right', on_delete=django.db.models.deletion.CASCADE, related_name='group_memberships', to='restapi.User'),
        ),
        migrations.AddField(
            model_name='group_share_right',
            name='group',
            field=models.ForeignKey(help_text='The group who will receive this share right', on_delete=django.db.models.deletion.CASCADE, related_name='group_share_rights', to='restapi.Group'),
        ),
        migrations.AddField(
            model_name='group_share_right',
            name='share',
            field=models.ForeignKey(help_text='The share that this share right grants permissions to', on_delete=django.db.models.deletion.CASCADE, related_name='group_share_rights', to='restapi.Share'),
        ),
        migrations.AlterUniqueTogether(
            name='user_group_membership',
            unique_together=set([('user', 'group')]),
        ),
        migrations.AlterUniqueTogether(
            name='group_share_right',
            unique_together=set([('group', 'share')]),
        ),
    ]
