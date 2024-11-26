from django.test import TestCase
from unittest.mock import patch, MagicMock
from .models import Restaurant, Menu, MenuSection, MenuItem, DietaryRestrictions, ProcessingLogs
from menu_manager.management.commands.etl_process import Command
import tempfile


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


