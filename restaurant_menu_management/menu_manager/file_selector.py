# file_selector.py
import tkinter as tk
from tkinter import filedialog

def get_pdf_file_path():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.update()  # Update the GUI to ensure it's ready
    file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )
    root.destroy()  # Destroy the Tkinter instance
    return file_path
