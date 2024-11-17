from django.core.management.base import BaseCommand
from django.db import connection
from menu_manager.models import Restaurant


class Command(BaseCommand):
    help = "Run raw SQL queries interactively"

    def handle(self, *args, **kwargs):
        # Step 1: Display available queries
        query_options = {
            1: "Retrieve Complete Menu Information",
            2: "Filter Items by Dietary Restrictions",
            3: "Track PDF Processing Status",
            4: "Generate Reports on Menu Items and Prices",
            5: "Handle Menu Updates and Versioning",
        }

        self.stdout.write("Available Queries:")
        for key, value in query_options.items():
            self.stdout.write(f"{key}: {value}")

        # Step 2: Ask the user to pick a query
        try:
            query_choice = int(input("Enter the number of the query you want to execute: "))
            if query_choice not in query_options:
                self.stdout.write(self.style.ERROR("Invalid choice. Exiting."))
                return
        except ValueError:
            self.stdout.write(self.style.ERROR("Invalid input. Exiting."))
            return

        # Step 3: Display all available restaurants
        restaurants = Restaurant.objects.all()
        if not restaurants.exists():
            self.stdout.write(self.style.ERROR("No restaurants available in the database."))
            return

        self.stdout.write("\nAvailable Restaurants:")
        for restaurant in restaurants:
            self.stdout.write(f"{restaurant.id}: {restaurant.name}")

        # Step 4: Ask the user to pick a restaurant
        try:
            restaurant_id = int(input("Enter the ID of the restaurant you want to use: "))
            if not Restaurant.objects.filter(id=restaurant_id).exists():
                self.stdout.write(self.style.ERROR("Invalid restaurant ID. Exiting."))
                return
        except ValueError:
            self.stdout.write(self.style.ERROR("Invalid input. Exiting."))
            return

        # Step 5: Execute the chosen query
        if query_choice == 1:
            self.get_complete_menu_information(restaurant_id)
        elif query_choice == 2:
            restriction_type = input("Enter the dietary restriction to filter by (e.g., Gluten-Free): ")
            self.filter_items_by_dietary_restrictions(restaurant_id, restriction_type)
        elif query_choice == 3:
            self.track_processing_status()
        elif query_choice == 4:
            self.generate_menu_item_price_report(restaurant_id)
        elif query_choice == 5:
            self.get_latest_menu_version(restaurant_id)

    def get_complete_menu_information(self, restaurant_id):
        query = """
        SELECT r.name AS restaurant_name, r.location, r.contact_number, r.email, r.website,
               m.version, m.status,
               s.section_name, s.description AS section_description,
               i.item_name, i.description AS item_description, i.price, i.availability_status
        FROM menu_manager_menu AS m
        JOIN menu_manager_restaurant AS r ON m.restaurant_id = r.id
        JOIN menu_manager_menusection AS s ON s.menu_id = m.id
        JOIN menu_manager_menuitem AS i ON i.section_id = s.id
        WHERE r.id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [restaurant_id])
            rows = cursor.fetchall()

        for row in rows:
            self.stdout.write(str(row))

    def filter_items_by_dietary_restrictions(self, restaurant_id, restriction_type):
        query = """
        SELECT i.item_name, i.description, i.price, d.restriction_type, d.notes
        FROM menu_manager_menuitem AS i
        JOIN menu_manager_dietaryrestrictions AS d ON d.item_id = i.id
        JOIN menu_manager_menusection AS s ON i.section_id = s.id
        JOIN menu_manager_menu AS m ON s.menu_id = m.id
        WHERE d.restriction_type = %s AND m.restaurant_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [restriction_type, restaurant_id])
            rows = cursor.fetchall()

        for row in rows:
            self.stdout.write(str(row))

    def track_processing_status(self):
        query = """
        SELECT p.menu_id, p.timestamp, p.status, p.error_message
        FROM menu_manager_processinglogs AS p
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.stdout.write(str(row))

    def generate_menu_item_price_report(self, restaurant_id):
        query = """
        SELECT i.item_name, i.price, i.availability_status
        FROM menu_manager_menuitem AS i
        JOIN menu_manager_menusection AS s ON i.section_id = s.id
        JOIN menu_manager_menu AS m ON s.menu_id = m.id
        WHERE m.restaurant_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [restaurant_id])
            rows = cursor.fetchall()

        self.stdout.write("Menu Items and Prices:")
        for row in rows:
            self.stdout.write(str(row))

        query_avg_price = """
        SELECT AVG(i.price)
        FROM menu_manager_menuitem AS i
        JOIN menu_manager_menusection AS s ON i.section_id = s.id
        JOIN menu_manager_menu AS m ON s.menu_id = m.id
        WHERE m.restaurant_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query_avg_price, [restaurant_id])
            avg_price = cursor.fetchone()[0]
        self.stdout.write(f"Average Price: {avg_price:.2f}")

    def get_latest_menu_version(self, restaurant_id):
        query = """
        SELECT m.id, m.version, m.status, m.created_date
        FROM menu_manager_menu AS m
        WHERE m.restaurant_id = %s
        ORDER BY m.created_date DESC
        LIMIT 1
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [restaurant_id])
            row = cursor.fetchone()

        if row:
            self.stdout.write(str(row))
        else:
            self.stdout.write("No menu found for the given restaurant.")
