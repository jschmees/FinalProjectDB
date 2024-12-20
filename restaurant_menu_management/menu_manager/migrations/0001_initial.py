# Generated by Django 5.1.3 on 2024-11-11 16:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('version', models.IntegerField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('archived', 'Archived')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('availability_status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=255)),
                ('contact_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=100)),
                ('website', models.URLField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DietaryRestrictions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restriction_type', models.CharField(max_length=50)),
                ('notes', models.TextField(blank=True, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu_manager.menuitem')),
            ],
        ),
        migrations.CreateModel(
            name='MenuSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu_manager.menu')),
            ],
        ),
        migrations.AddField(
            model_name='menuitem',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu_manager.menusection'),
        ),
        migrations.CreateModel(
            name='ProcessingLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('processed', 'Processed'), ('error', 'Error')], max_length=20)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu_manager.menu')),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu_manager.restaurant'),
        ),
    ]
