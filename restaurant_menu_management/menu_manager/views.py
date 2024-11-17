from django.shortcuts import render

from django.shortcuts import render
from .queries import (
    get_complete_menu_information,
    filter_items_by_dietary_restrictions,
    track_processing_status,
    generate_menu_item_price_report,
    get_latest_menu_version,
)

def menu_detail(request, menu_id):
    menu_info = get_complete_menu_information(menu_id)
    return render(request, 'menu_manager/restaurant_menus.html', {'menu_info': menu_info})

def dietary_restrictions(request, restriction_type):
    items = filter_items_by_dietary_restrictions(restriction_type)
    return render(request, 'menu_manager/menu_items.html', {'items': items})

def processing_logs(request):
    logs = track_processing_status()
    return render(request, 'menu_manager/processing_logs.html', {'logs': logs})

def price_report(request):
    report = generate_menu_item_price_report()
    return render(request, 'menu_manager/menu_items.html', {'report': report})

