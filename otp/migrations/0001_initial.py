# Generated by Django 4.2.6 on 2023-10-15 06:35

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VerifyPhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('otp', models.TextField()),
                ('otp_for', models.CharField(choices=[('N', 'NEW_ACCOUNT')], max_length=1)),
                ('expire_at', models.DateTimeField()),
            ],
        ),
    ]
