"""
Main Window
"""

from pathlib import Path
from tkinter import filedialog
import webbrowser
import customtkinter as ctk
import sys
import ctypes

from functions.qr import generate_qr
from ui.utils.window import center_window, resource_path

class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        if sys.platform.startswith("win"):
            myappid = "up0k.qrcodegenerator.app.1.0"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.title("Up0k Qrcode")
        self.iconbitmap(resource_path("icon.ico"))

        center_window(self, 600, 420)
        self.minsize(550, 400)

        self.create_layout()

    def create_layout(self):

        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self, text="QR Code Generator", font=("Consolas", 20, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.text_entry = ctk.CTkEntry(
            self, placeholder_text="Enter text or Url..."
        )
        self.text_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.filename_entry = ctk.CTkEntry(
            self, placeholder_text="Custom filename (default: qrcode)"
        )
        self.filename_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # Save Directory Selection
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.path_frame.grid_columnconfigure(0, weight=1)

        self.path_label = ctk.CTkLabel(
            self.path_frame,
            text="Save Location: Default (.exe folder)",
            anchor="w",
        )
        self.path_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.browse_btn = ctk.CTkButton(
            self.path_frame,
            text="Browse...",
            width=100,
            command=self.on_browse_click,
        )
        self.browse_btn.grid(row=0, column=1, padx=10, pady=10)

        # Generate Button
        self.generate_btn = ctk.CTkButton(
            self, text="Generate QR Code", command=self.on_generate_click
        )
        self.generate_btn.grid(row=4, column=0, padx=20, pady=15)

        # Status Label (replacing terminal print())
        self.status_label = ctk.CTkLabel(self, text="", text_color="green")
        self.status_label.grid(row=5, column=0, padx=20, pady=5)

        self.watermark_label = ctk.CTkLabel(
            self, text="Made by Up0k", font=("Monospace", 13, "bold"), text_color="#D0FE1D"
        )
        self.watermark_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-5)
        self.watermark_label.bind("<button-1>", lambda event: webbrowser.open("https://github.com/Upok18"))

    def on_browse_click(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.selected_path = folder_selected
            self.path_label.configure(text=f"Save Location: {folder_selected}")

    def on_generate_click(self):
        user_text = self.text_entry.get()
        custom_name = self.filename_entry.get()

        if not user_text.strip():
            self.status_label.configure(
                text="Error: Enter text or URL first!", text_color="red"
            )
            return

        try:
            saved_file = generate_qr(
                text=user_text,
                filename=custom_name,
                save_dir=self.selected_path,
            )
            self.status_label.configure(
                text=f"QR Code saved as {saved_file}", text_color="green"
            )
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}", text_color="red")