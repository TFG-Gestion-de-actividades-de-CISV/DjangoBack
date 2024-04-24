# Generated by Django 5.0.3 on 2024-04-23 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_user', '0006_profile_city_profile_name_profile_second_surname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='birthdate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='postal_code',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
