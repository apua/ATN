# Generated by Django 2.0.2 on 2018-02-27 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_result_create_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='suite',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Suite'),
        ),
    ]