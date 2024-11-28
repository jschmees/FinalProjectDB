from menu_manager.models import Menu, MenuItem, DietaryRestrictions, ProcessingLogs

def get_complete_menu_information(menu_id):
    try:
        menu = Menu.objects.get(pk=menu_id)
        items = MenuItem.objects.filter(section__menu=menu)
        return {
            'menu': menu,
            'items': items
        }
    except Menu.DoesNotExist:
        return None

def filter_items_by_dietary_restrictions(restriction_type):
    return MenuItem.objects.filter(dietaryrestrictions__restriction_type=restriction_type)

def track_processing_status():
    return ProcessingLogs.objects.all()

def generate_menu_item_price_report():
    return MenuItem.objects.values('item_name', 'price')

def get_latest_menu_version(restaurant_id):
    return Menu.objects.filter(restaurant__id=restaurant_id).order_by('-version').first()
