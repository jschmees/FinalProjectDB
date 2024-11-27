# Generated by Django 4.2.6 on 2024-11-27 20:29

from django.db import migrations


from django.db import migrations, connection

def create_trigger(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute("""
        CREATE TRIGGER log_menuitem_insert
        AFTER INSERT ON menu_manager_menuitem
        FOR EACH ROW
        BEGIN
            INSERT INTO menu_manager_processinglogs (menu_id, timestamp, status, error_message)
            VALUES (NEW.section_id, NOW(), 'processed', '');
        END;
        """)

def drop_trigger(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute("""
        DROP TRIGGER IF EXISTS log_menuitem_insert;
        """)

class Migration(migrations.Migration):

    dependencies = [
        ('menu_manager', '0005_alter_processinglogs_menu'),  # Replace 'previous_migration_name' with the actual name of your last migration
    ]

    operations = [
        migrations.RunPython(create_trigger, reverse_code=drop_trigger),
    ]
