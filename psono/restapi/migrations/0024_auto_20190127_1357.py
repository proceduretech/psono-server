# Generated by Django 2.1.5 on 2019-01-27 13:57

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0023_auto_20190107_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('chunk_count', models.IntegerField(help_text='The amount of chunks', verbose_name='Chunk Count')),
                ('size', models.BigIntegerField(help_text='The size of the files in bytes (including encryption overhead)', verbose_name='Size')),
                ('delete_date', models.DateTimeField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='File_Chunk',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('hash_checksum', models.CharField(max_length=128, unique=True)),
                ('position', models.IntegerField(help_text='The position of the chunk in the file', verbose_name='Position')),
                ('size', models.BigIntegerField(help_text='The size of the chunk in bytes (including encryption overhead)', verbose_name='Size')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_chunk', to='restapi.File')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='File_Link',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('link_id', models.UUIDField(unique=True)),
                ('file', models.ForeignKey(help_text='The file, that this link links to.', on_delete=django.db.models.deletion.CASCADE, related_name='links', to='restapi.File')),
                ('parent_datastore', models.ForeignKey(help_text='The datastore, where this link ends', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='restapi.Data_Store')),
                ('parent_share', models.ForeignKey(help_text='The share, where this link ends and gets its permissions from', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='restapi.Share')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='File_Transfer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(default='download', max_length=8)),
                ('credit', models.DecimalField(decimal_places=16, default=Decimal('0'), max_digits=24)),
                ('size', models.BigIntegerField(help_text='The amount in bytes that will be transferred (including encryption overhead)', verbose_name='Size')),
                ('size_transferred', models.BigIntegerField(help_text='The amount in bytes that have been transferred (including encryption overhead)', verbose_name='Transferred Size')),
                ('chunk_count', models.IntegerField(help_text='The amount of chunks', verbose_name='Chunk Count')),
                ('chunk_count_transferred', models.IntegerField(help_text='The amount of chunks already transfered', verbose_name='Chunk Count Transfered')),
                ('file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_transfer', to='restapi.File')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fileserver_Cluster',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('file_size_limit', models.BigIntegerField(help_text='File size limit in bytes', verbose_name='File size limit')),
                ('auth_public_key', models.CharField(help_text='Public key given to fileservers of this cluster to authenticate against the server', max_length=256, verbose_name='public key')),
                ('auth_private_key', models.CharField(help_text='Private key used to validate the request of the ', max_length=256, verbose_name='private key')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fileserver_Cluster_Member_Shard_Link',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('read', models.BooleanField(default=True, help_text='Weather this shard accepts reads', verbose_name='Read')),
                ('write', models.BooleanField(default=True, help_text='Weather this shard accepts writes', verbose_name='Write')),
                ('delete', models.BooleanField(default=True, help_text='Weather this shard accepts delete jobs', verbose_name='Delete')),
                ('ip_read_whitelist', models.CharField(help_text='IP Whitelist for read operations', max_length=2048, null=True, verbose_name='IP read whitelist')),
                ('ip_write_whitelist', models.CharField(help_text='IP Whitelist for write operations', max_length=2048, null=True, verbose_name='IP write whitelist')),
                ('ip_read_blacklist', models.CharField(help_text='IP Blacklist for read operations', max_length=2048, null=True, verbose_name='IP read blacklist')),
                ('ip_write_blacklist', models.CharField(help_text='IP Blacklist for write operations', max_length=2048, null=True, verbose_name='IP write blacklist')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fileserver_Cluster_Members',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('create_ip', models.GenericIPAddressField()),
                ('key', models.CharField(max_length=128, unique=True)),
                ('public_key', models.CharField(help_text='Public key of the member that is sent to the client', max_length=256, verbose_name='public key')),
                ('secret_key', models.CharField(help_text='Symmetric Key for the transport encryption', max_length=256, verbose_name='Secret Key')),
                ('url', models.CharField(max_length=256, verbose_name='Public URL')),
                ('read', models.BooleanField(default=True, help_text='Weather this server accepts reads', verbose_name='Read')),
                ('write', models.BooleanField(default=True, help_text='Weather this server accepts writes', verbose_name='Write')),
                ('delete', models.BooleanField(default=True, help_text='Weather this server accepts deletes', verbose_name='Delete')),
                ('valid_till', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('fileserver_cluster', models.ForeignKey(help_text='The cluster this member belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='members', to='restapi.Fileserver_Cluster')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fileserver_Cluster_Shard_Link',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('read', models.BooleanField(default=True, help_text='Weather this shard accepts reads', verbose_name='Read')),
                ('write', models.BooleanField(default=True, help_text='Weather this shard accepts writes', verbose_name='Write')),
                ('delete', models.BooleanField(default=True, help_text='Weather this connection accepts deletes', verbose_name='Delete')),
                ('cluster', models.ForeignKey(help_text='The cluster this shard belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='links', to='restapi.Fileserver_Cluster')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fileserver_Shard',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('active', models.BooleanField(default=True, help_text='Specifies if the shard is offline or online', verbose_name='Activated')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='user',
            name='credit',
            field=models.DecimalField(decimal_places=16, default=Decimal('0'), max_digits=24),
        ),
        migrations.AlterField(
            model_name='secret_link',
            name='secret',
            field=models.ForeignKey(help_text='The secret, that this link links to.', on_delete=django.db.models.deletion.CASCADE, related_name='links', to='restapi.Secret'),
        ),
        migrations.AddField(
            model_name='fileserver_cluster_shard_link',
            name='shard',
            field=models.ForeignKey(help_text='The shard this cluster belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='links', to='restapi.Fileserver_Shard'),
        ),
        migrations.AddField(
            model_name='fileserver_cluster_member_shard_link',
            name='member',
            field=models.ForeignKey(help_text='The cluster member this link belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='member_links', to='restapi.Fileserver_Cluster_Members'),
        ),
        migrations.AddField(
            model_name='fileserver_cluster_member_shard_link',
            name='shard',
            field=models.ForeignKey(help_text='The shard this link belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='member_links', to='restapi.Fileserver_Shard'),
        ),
        migrations.AddField(
            model_name='file_transfer',
            name='shard',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_transfer', to='restapi.Fileserver_Shard'),
        ),
        migrations.AddField(
            model_name='file_transfer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_transfer', to='restapi.User'),
        ),
        migrations.AddField(
            model_name='file_chunk',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_chunk', to='restapi.User'),
        ),
        migrations.AddField(
            model_name='file',
            name='shard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file', to='restapi.Fileserver_Shard'),
        ),
        migrations.AddField(
            model_name='file',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file', to='restapi.User'),
        ),
        migrations.AlterUniqueTogether(
            name='fileserver_cluster_shard_link',
            unique_together={('cluster', 'shard')},
        ),
        migrations.AlterUniqueTogether(
            name='fileserver_cluster_member_shard_link',
            unique_together={('member', 'shard')},
        ),
        migrations.AlterUniqueTogether(
            name='file_chunk',
            unique_together={('position', 'file')},
        ),
    ]
