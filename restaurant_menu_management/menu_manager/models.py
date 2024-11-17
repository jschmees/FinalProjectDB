from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    website = models.URLField(max_length=100)

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('archived', 'Archived')])

class MenuSection(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    section_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

class MenuItem(models.Model):
    section = models.ForeignKey(MenuSection, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability_status = models.BooleanField(default=True)

class DietaryRestrictions(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    restriction_type = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)

class ProcessingLogs(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('processed', 'Processed'), ('error', 'Error')])
    error_message = models.TextField(blank=True, null=True)


