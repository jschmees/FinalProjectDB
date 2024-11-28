from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.full_text_search_view, name='full_text_search'),
]
