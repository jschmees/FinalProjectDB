from django.contrib import admin
from .models import Restaurant, Menu, MenuSection, MenuItem, DietaryRestrictions, ProcessingLogs

admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(MenuSection)
admin.site.register(MenuItem)
admin.site.register(DietaryRestrictions)
admin.site.register(ProcessingLogs)

