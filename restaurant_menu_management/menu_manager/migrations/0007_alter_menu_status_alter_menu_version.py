# Generated by Django 4.2.6 on 2024-11-28 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_manager', '0006_add_sql_triggers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('archived', 'Archived'), ('draft', 'Draft')], max_length=20),
        ),
        migrations.AlterField(
            model_name='menu',
            name='version',
            field=models.IntegerField(default=1),
        ),
    ]