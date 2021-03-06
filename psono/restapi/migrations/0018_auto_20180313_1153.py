# Generated by Django 2.0.2 on 2018-03-13 11:53

from django.db import migrations

def update_duo_enabled(apps, schema_editor):
    Duo = apps.get_model('restapi', 'Duo')
    for duo in Duo.objects.filter(active=True).all():
        duo.user.duo_enabled = True
        duo.user.save()

def update_google_authenticator_enabled(apps, schema_editor):
    Google_Authenticator = apps.get_model('restapi', 'Google_Authenticator')
    for ga in Google_Authenticator.objects.filter(active=True).all():
        ga.user.google_authenticator_enabled = True
        ga.user.save()

def update_yubikey_otp_enabled(apps, schema_editor):
    Yubikey_OTP = apps.get_model('restapi', 'Yubikey_OTP')
    for yubikey in Yubikey_OTP.objects.filter(active=True).all():
        yubikey.user.yubikey_otp_enabled = True
        yubikey.user.save()



class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0017_auto_20180313_1135'),
    ]

    operations = [
        migrations.RunPython(update_duo_enabled),
        migrations.RunPython(update_google_authenticator_enabled),
        migrations.RunPython(update_yubikey_otp_enabled),
    ]
