from django.test import TestCase
from unittest.mock import patch, MagicMock
from menu_manager.models import Restaurant, Menu, MenuSection, MenuItem, DietaryRestrictions, ProcessingLogs
from menu_manager.management.commands.etl_process import Command
import json


class RestaurantMenuTestCase(TestCase):

    def setUp(self):
        # Set up test data
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            location="123 Main St",
            contact_number="1234567890",
            email="test@restaurant.com",
            website="http://restaurant.com"
        )
        self.menu = Menu.objects.create(restaurant=self.restaurant, version=1, status="active")
        self.section = MenuSection.objects.create(menu=self.menu, section_name="Starters")
        self.item = MenuItem.objects.create(
            section=self.section, item_name="Salad", description="Fresh Salad", price=5.99, availability_status=True
        )
        self.restriction = DietaryRestrictions.objects.create(item=self.item, restriction_type="Vegan")

    def test_restaurant_creation(self):
        self.assertEqual(self.restaurant.name, "Test Restaurant")
        self.assertEqual(self.restaurant.location, "123 Main St")

    def test_menu_association_with_restaurant(self):
        self.assertEqual(self.menu.restaurant, self.restaurant)

    def test_menu_section_association(self):
        self.assertEqual(self.section.menu, self.menu)

    def test_menu_item_association(self):
        self.assertEqual(self.item.section, self.section)

    def test_dietary_restriction(self):
        self.assertEqual(self.restriction.restriction_type, "Vegan")
        self.assertEqual(self.restriction.item, self.item)

    def test_menu_item_price(self):
        self.assertTrue(self.item.price > 0, "Price should be greater than zero")




class ETLProcessCommandTest(TestCase):

    def setUp(self):
        # Sample structured JSON data returned by AI
        self.sample_data = {
            "restaurant": {
                "name": "Sample Restaurant",
                "location": "123 Sample St",
                "contact_number": "123-456-7890",
                "email": "sample@example.com",
                "website": "https://www.samplerestaurant.com"
            },
            "menu": {
                "version": 1,
                "status": "active"
            },
            "menu_sections": [
                {
                    "section_name": "Appetizers",
                    "description": "Start your meal off right",
                    "items": [
                        {
                            "item_name": "Spring Rolls",
                            "description": "Crispy and delicious",
                            "price": "5.99",
                            "availability_status": True
                        }
                    ]
                }
            ],
            "dietary_restrictions": [
                {
                    "item_name": "Spring Rolls",
                    "restriction_type": "Vegan",
                    "notes": "No animal products"
                }
            ]
        }

    @patch('menu_manager.management.commands.etl_process.get_pdf_file_path')
    @patch('pdfplumber.open')
    def test_extract_text_from_pdf(self, mock_pdfplumber_open, mock_get_pdf_file_path):
        # Mock PDF file path
        mock_get_pdf_file_path.return_value = "mock_file_path.pdf"

        # Mock PDF extraction
        mock_pdf = MagicMock()
        mock_pdf.pages = [MagicMock(extract_text=MagicMock(return_value="Sample text"))]
        mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf

        command = Command()
        text = command.extract_text_from_pdf("mock_file_path.pdf")

        self.assertEqual(text, "Sample text")
        mock_pdfplumber_open.assert_called_once_with("mock_file_path.pdf")

    @patch('openai.ChatCompletion.create')
    def test_process_with_ai(self, mock_chat_completion_create):
        # Mock OpenAI response
        mock_chat_completion_create.return_value = {
            'choices': [
                {'message': {'content': json.dumps(self.sample_data)}}
            ]
        }

        command = Command()
        structured_data_text = command.process_with_ai("Sample text")

        self.assertEqual(json.loads(structured_data_text), self.sample_data)
        mock_chat_completion_create.assert_called_once()

    def test_parse_json(self):
        command = Command()
        structured_data = command.parse_json(json.dumps(self.sample_data))

        self.assertEqual(structured_data, self.sample_data)

    def test_validate_data(self):
        command = Command()
        is_valid, message = command.validate_data(self.sample_data)

        self.assertTrue(is_valid)
        self.assertEqual(message, "Data is valid")



    @patch('menu_manager.management.commands.etl_process.get_pdf_file_path')
    @patch('pdfplumber.open')
    @patch('openai.ChatCompletion.create')
    def test_handle(self, mock_chat_completion_create, mock_pdfplumber_open, mock_get_pdf_file_path):
        # Mock dependencies
        mock_get_pdf_file_path.return_value = "mock_file_path.pdf"
        mock_pdf = MagicMock()
        mock_pdf.pages = [MagicMock(extract_text=MagicMock(return_value="Sample text"))]
        mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf
        mock_chat_completion_create.return_value = {
            'choices': [
                {'message': {'content': json.dumps(self.sample_data)}}
            ]
        }

        command = Command()
        command.handle()

        # Verify that data was inserted
        restaurant = Restaurant.objects.get(name="Sample Restaurant")
        self.assertIsNotNone(restaurant)

        # Verify ProcessingLogs
        log = ProcessingLogs.objects.get(menu__restaurant=restaurant)
        self.assertEqual(log.status, "processed")
        self.assertEqual(log.error_message, "")

