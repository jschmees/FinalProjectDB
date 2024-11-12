import pdfplumber
from django.core.management.base import BaseCommand
import openai

class Command(BaseCommand):
    help = "Extracts text from a menu PDF and prepares it for AI processing"

    def handle(self, *args, **kwargs):
        # PDF Extraction
        try:
            with pdfplumber.open("/Users/jannikschmees/PycharmProjects/FinalProjectDB/restaurant_menu_management/menu_manager/pdf_files/thehatmenu_eng.pdf") as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
            self.stdout.write("PDF extraction complete")
        except Exception as e:
            self.stdout.write(f"PDF extraction failed: {e}")





