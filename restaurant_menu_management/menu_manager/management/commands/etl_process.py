import pdfplumber
from django.core.management.base import BaseCommand
import openai
import os
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
            structured_data = self.process_with_ai(text)
            self.stdout.write(f"Structured data from AI:\n{structured_data}")

            # Step 3: Validate data
            is_valid, message = self.validate_data(structured_data)
            if is_valid:
                # Step 4: Insert data into the database
                self.insert_data(structured_data)
            else:
                self.stdout.write(self.style.ERROR(f"Data validation failed: {message}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"PDF extraction or AI processing failed: {e}"))

    def process_with_ai(self, text):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are an assistant that extracts structured menu data."},
                {"role": "user", "content": f"Extract and structure menu data from the following text according to this format:\n\n"
                                            f"Restaurant:\n"
                                            f"- name: (text)\n"
                                            f"- location: (text)\n"
                                            f"- contact_number: (text)\n"
                                            f"- email: (text)\n"
                                            f"- website: (text)\n\n"
                                            f"Menu:\n"
                                            f"- version: (integer)\n"
                                            f"- status: ('active' or 'archived')\n"
                                            f"MenuSections:\n"
                                            f"- section_name: (text)\n"
                                            f"- description: (text)\n"
                                            f"MenuItems:\n"
                                            f"- item_name: (text)\n"
                                            f"- description: (text)\n"
                                            f"- price: (decimal)\n"
                                            f"- availability_status: (boolean)\n"
                                            f"DietaryRestrictions:\n"
                                            f"- restriction_type: (text)\n"
                                            f"- notes: (text)\n\n"
                                            f"Text:\n{text}"}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        return response['choices'][0]['message']['content']

    def validate_data(self, data):
        # Check Restaurant fields
        if not all(key in data for key in ["name", "location", "contact_number", "email", "website"]):
            return False, "Missing Restaurant fields"

        # Check Menu fields
        if not all(key in data.get("menu", {}) for key in ["version", "status"]):
            return False, "Missing Menu fields"

        # Check Menu Sections
        for section in data.get("menu_sections", []):
            if not all(key in section for key in ["section_name", "description"]):
                return False, f"Missing fields in Menu Section: {section}"

            # Check Menu Items
            for item in section.get("items", []):
                if not all(key in item for key in ["item_name", "description", "price", "availability_status"]):
                    return False, f"Missing fields in Menu Item: {item}"

        # Check Dietary Restrictions
        for restriction in data.get("dietary_restrictions", []):
            if not all(key in restriction for key in ["restriction_type", "notes"]):
                return False, f"Missing fields in Dietary Restrictions: {restriction}"

        return True, "Data is valid"

    def insert_data(self, data):
        try:
            # Insert Restaurant data
            restaurant, _ = Restaurant.objects.get_or_create(
                name=data["name"],
                location=data["location"],
                contact_number=data["contact_number"],
                email=data["email"],
                website=data["website"]
            )

            # Insert Menu data
            menu = Menu.objects.create(
                restaurant=restaurant,
                version=data["menu"]["version"],
                status=data["menu"]["status"]
            )

            # Insert Menu Sections and Items
            for section_data in data["menu_sections"]:
                section = MenuSection.objects.create(
                    menu=menu,
                    section_name=section_data["section_name"],
                    description=section_data.get("description", "")
                )

                for item_data in section_data["items"]:
                    MenuItem.objects.create(
                        section=section,
                        item_name=item_data["item_name"],
                        description=item_data.get("description", ""),
                        price=item_data["price"],
                        availability_status=item_data["availability_status"]
                    )

            # Insert Dietary Restrictions
            for restriction_data in data.get("dietary_restrictions", []):
                item = MenuItem.objects.get(item_name=restriction_data["item_name"])  # Assuming 'item_name' for lookup
                DietaryRestrictions.objects.create(
                    item=item,
                    restriction_type=restriction_data["restriction_type"],
                    notes=restriction_data.get("notes", "")
                )

            self.stdout.write(self.style.SUCCESS("Data inserted successfully."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Data insertion failed: {e}"))
