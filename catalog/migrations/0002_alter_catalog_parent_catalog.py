# Generated by Django 4.1 on 2022-08-06 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalog',
            name='parent_catalog',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='catalog.catalog'),
        ),
    ]
