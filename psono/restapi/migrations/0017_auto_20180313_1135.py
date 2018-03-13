# Generated by Django 2.0.2 on 2018-03-13 11:35

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0016_auto_20180310_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='duo_enabled',
            field=models.BooleanField(default=False, help_text='True once duo 2fa is enabled', verbose_name='Duo 2FA enabled'),
        ),
        migrations.AddField(
            model_name='user',
            name='google_authenticator_enabled',
            field=models.BooleanField(default=False, help_text='True once ga 2fa is enabled', verbose_name='GA 2FA enabled'),
        ),
        migrations.AddField(
            model_name='user',
            name='yubikey_otp_enabled',
            field=models.BooleanField(default=False, help_text='True once yubikey 2fa is enabled', verbose_name='Yubikey OTP 2FA enabled'),
        ),
    ]