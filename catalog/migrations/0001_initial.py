# Generated by Django 4.1 on 2022-08-06 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('parent_catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='catalog.catalog')),
            ],
        ),
    ]