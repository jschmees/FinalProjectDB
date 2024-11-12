import pdfplumber
from django.core.management.base import BaseCommand
import openai
import os

class Command(BaseCommand):
    help = "Extracts text from a menu PDF and prepares it for AI processing"

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

        except Exception as e:
            self.stdout.write(f"PDF extraction or AI processing failed: {e}")

    def process_with_ai(self, text):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are an assistant that extracts structured menu data."},
                {"role": "user", "content": "Extract structured menu data from the following text:\n" + text}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        return response['choices'][0]['message']['content']
