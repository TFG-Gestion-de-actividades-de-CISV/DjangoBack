# Generated by Django 5.0.3 on 2024-06-02 19:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='colaborador',
            name='cisv_safeguarding',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cisv_safeguarding', to='activities.document'),
        ),
        migrations.AddField(
            model_name='colaborador',
            name='criminal_crimes_certificate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='criminal_crimes_certificate', to='activities.document'),
        ),
        migrations.AddField(
            model_name='colaborador',
            name='sexual_crimes_certificate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sexual_crimes_certificate', to='activities.document'),
        ),
        migrations.AddField(
            model_name='lider',
            name='health_card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lider_health_card', to='activities.document'),
        ),
        migrations.AddField(
            model_name='monitor',
            name='health_card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='monitor_health_card', to='activities.document'),
        ),
        migrations.AddField(
            model_name='monitor',
            name='pago',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='monitor_pago', to='activities.document'),
        ),
    ]