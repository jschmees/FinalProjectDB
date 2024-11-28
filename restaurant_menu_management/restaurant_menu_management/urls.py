from django.contrib import admin
from django.urls import path, include  # Import `include` to include the app URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu_manager/', include('menu_manager.urls')),  # Include the URLs from `menu_manager`
]
