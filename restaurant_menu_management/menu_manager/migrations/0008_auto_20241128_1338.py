from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('menu_manager', '0007_alter_menu_status_alter_menu_version'),  # Update with the correct previous migration name
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE menu_manager_restaurant ADD FULLTEXT(name, location);"
        ),
        migrations.RunSQL(
            "ALTER TABLE menu_manager_menuitem ADD FULLTEXT(item_name, description);"
        ),
    ]
