import pdfplumber
from django.core.management.base import BaseCommand
import openai
import os
import json
from menu_manager.models import Restaurant, Menu, MenuSection, MenuItem, DietaryRestrictions


class Command(BaseCommand):
    help = "Extracts text from a menu PDF, processes it with AI, validates, and inserts it into the database."

    def handle(self, *args, **kwargs):
        # Step 1: PDF Extraction
        try:
            with pdfplumber.open("/Users/jannikschmees/PycharmProjects/FinalProjectDB/restaurant_menu_management/menu_manager/pdf_files/thehatmenu_eng.pdf") as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
            self.stdout.write("PDF extraction complete")

            # Step 2: Process extracted text with AI
            structured_data_text = self.process_with_ai(text)
            self.stdout.write(f"AI Response:\n{structured_data_text}")

            # Parse the AI response as JSON
            try:
                structured_data = json.loads(structured_data_text)
                self.stdout.write("AI response parsed as JSON successfully.")
            except json.JSONDecodeError as e:
                self.stdout.write(self.style.ERROR(f"Failed to parse AI response as JSON: {e}"))
                structured_data = None

            # Step 3: Validate data if parsing was successful
            if structured_data:
                is_valid, message = self.validate_data(structured_data)
                if is_valid:
                    # Step 4: Insert data into the database
                    self.insert_data(structured_data)
                else:
                    self.stdout.write(self.style.ERROR(f"Data validation failed: {message}"))
            else:
                self.stdout.write(self.style.ERROR("No structured data to process."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"ETL process failed: {e}"))

    def process_with_ai(self, text):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that extracts structured menu data and returns it in strict JSON format without any extra text."
                },
                {
                    "role": "user",
                    "content": (
                        f"Extract and structure menu data from the following text. "
                        f"Return the data in JSON format matching this structure:\n\n"
                        f"{{\n"
                        f"  \"restaurant\": {{\n"
                        f"    \"name\": \"...\",\n"
                        f"    \"location\": \"...\",\n"
                        f"    \"contact_number\": \"...\",\n"
                        f"    \"email\": \"...\",\n"
                        f"    \"website\": \"...\"\n"
                        f"  }},\n"
                        f"  \"menu\": {{\n"
                        f"    \"version\": 1,\n"
                        f"    \"status\": \"active\"\n"
                        f"  }},\n"
                        f"  \"menu_sections\": [\n"
                        f"    {{\n"
                        f"      \"section_name\": \"...\",\n"
                        f"      \"description\": \"...\",\n"
                        f"      \"items\": [\n"
                        f"        {{\n"
                        f"          \"item_name\": \"...\",\n"
                        f"          \"description\": \"...\",\n"
                        f"          \"price\": \"...\",\n"
                        f"          \"availability_status\": true\n"
                        f"        }}\n"
                        f"      ]\n"
                        f"    }}\n"
                        f"  ],\n"
                        f"  \"dietary_restrictions\": [\n"
                        f"    {{\n"
                        f"      \"item_name\": \"...\",\n"
                        f"      \"restriction_type\": \"...\",\n"
                        f"      \"notes\": \"...\"\n"
                        f"    }}\n"
                        f"  ]\n"
                        f"}}\n\n"
                        f"Text:\n{text}"
                    )
                }
            ],
            temperature=0.5,
            max_tokens=2000
        )
        return response['choices'][0]['message']['content']

    def validate_data(self, data):
        # Check Restaurant fields
        restaurant = data.get("restaurant", {})
        if not all(key in restaurant for key in ["name", "location", "contact_number", "email", "website"]):
            return False, "Missing Restaurant fields"

        # Check Menu fields
        menu = data.get("menu", {})
        if not all(key in menu for key in ["version", "status"]):
            return False, "Missing Menu fields"

        # Check Menu Sections
        for section in data.get("menu_sections", []):
            if not all(key in section for key in ["section_name", "description", "items"]):
                return False, f"Missing fields in Menu Section: {section}"

            # Check Menu Items
            for item in section.get("items", []):
                if not all(key in item for key in ["item_name", "description", "price", "availability_status"]):
                    return False, f"Missing fields in Menu Item: {item}"

        # Check Dietary Restrictions
        for restriction in data.get("dietary_restrictions", []):
            if not all(key in restriction for key in ["item_name", "restriction_type", "notes"]):
                return False, f"Missing fields in Dietary Restrictions: {restriction}"

        return True, "Data is valid"

    def insert_data(self, data):
        try:
            # Insert Restaurant data
            restaurant_data = data["restaurant"]
            restaurant, _ = Restaurant.objects.get_or_create(
                name=restaurant_data["name"],
                defaults={
                    "location": restaurant_data["location"],
                    "contact_number": restaurant_data["contact_number"],
                    "email": restaurant_data["email"],
                    "website": restaurant_data["website"],
                }
            )

            # Insert Menu data
            menu_data = data["menu"]
            menu = Menu.objects.create(
                restaurant=restaurant,
                version=menu_data["version"],
                status=menu_data["status"]
            )

            # Insert Menu Sections and Items
            for section_data in data["menu_sections"]:
                section = MenuSection.objects.create(
                    menu=menu,
                    section_name=section_data["section_name"],
                    description=section_data.get("description", "")
                )

                for item_data in section_data["items"]:
                    # Normalize price format
                    price_str = item_data["price"].replace('€', '').replace(',', '.').strip()
                    price = float(price_str) if price_str else 0.0  # Default to 0.0 if price is empty

                    menu_item = MenuItem.objects.create(
                        section=section,
                        item_name=item_data["item_name"],
                        description=item_data.get("description", ""),
                        price=price,
                        availability_status=item_data["availability_status"]
                    )

                    # Check if dietary restrictions are provided for the item
                    dietary_restrictions = item_data.get("dietary_restrictions", [])
                    for restriction in dietary_restrictions:
                        DietaryRestrictions.objects.create(
                            item=menu_item,
                            restriction_type=restriction.get("restriction_type", ""),
                            notes=restriction.get("notes", "")
                        )

            self.stdout.write(self.style.SUCCESS("Data inserted successfully."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Data insertion failed: {e}"))
