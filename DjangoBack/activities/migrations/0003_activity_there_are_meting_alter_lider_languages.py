# Generated by Django 5.0.3 on 2024-06-08 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='there_are_meting',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='lider',
            name='languages',
            field=models.TextField(),
        ),
    ]
