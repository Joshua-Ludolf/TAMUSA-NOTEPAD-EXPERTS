"""
    Group: TAMUSA Notepad Experts (TNE)
    Authors: Joshua Ludolf & Luis Morales
    Class: CSCI 3366 - Programming Languages
"""

import tkinter as tk
from tkinter import scrolledtext, Menu
import file  # Import the file operations module

class NotePad:
    """
    A class to represent a Notepad application.
    Attributes
    ----------
    root : Tk
        The root window of the application.
    current_file : list
        A list to hold the current file path.
    Methods
    -------
    __init__(root):
        Initializes the Notepad application with the given root window.
    create_widgets():
        Creates and configures the widgets for the Notepad application.
    create_menu_bar():
        Creates and configures the menu bar for the Notepad application.
    """
    def __init__(self, root):
        self.root = root
        self.root.geometry("1920x1080")
        self.root.title("TAMUSA Notepad")
        self.root.configure(bg="#1a1a1a")  # Dark background for the main window
        self.root.font = ("Cascadia Code", 12)  # Modern coding font
        self.root.iconbitmap("tne.ico")
        self.current_file = [None]
        self.create_widgets()

    def create_widgets(self):
        # Create main container frame
        self.main_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.create_menu_bar()
        
        # Text editor with enhanced styling
        self.message_box = scrolledtext.ScrolledText(
            self.main_frame,
            font=("Cascadia Code", 12),  # Font as tuple
            wrap=tk.WORD,
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#23c4a4",
            selectbackground="#264f78",
            selectforeground="#ffffff",
            padx=10,
            pady=10
        )
        self.message_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        # Create status bar
        self.status_bar = tk.Label(
            self.main_frame,
            text="Ready",
            bg="#2d2d2d",
            fg="#23c4a4",
            font=("Cascadia Code", 10),
            anchor=tk.W,
            padx=10,
            pady=5
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=(0, 5))

        # Bind events for status updates
        self.message_box.bind("<KeyPress>", self.update_status)
        self.message_box.bind("<KeyRelease>", self.update_status)

    def create_menu_bar(self):
        menu_bar = Menu(
            self.root,
            bg="#2d2d2d",
            fg="#ffffff",
            activebackground="#3e3e3e",
            activeforeground="#23c4a4",
            font=("Cascadia Code", 11),
            relief=tk.FLAT,
            borderwidth=0
        )
        self.root.config(menu=menu_bar)

        # File menu with enhanced styling
        file_menu = Menu(
            menu_bar,
            tearoff=0,
            bg="#2d2d2d",
            fg="#ffffff",
            activebackground="#3e3e3e",
            activeforeground="#23c4a4",
            font=("Cascadia Code", 11),
            relief=tk.FLAT,
            borderwidth=0
        )
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Add menu items with modern styling
        for label, command in [
            ("New", lambda: file.new_file(self.message_box, self.current_file)),
            ("Save", lambda: self.save_file()),
            ("Save As", lambda: file.save_file_as(self.message_box, self.current_file)),
            ("Open", lambda: file.open_file(self.message_box, self.current_file))
        ]:
            file_menu.add_command(
                label=label,
                command=command,
                font=("Cascadia Code", 11),
                compound=tk.LEFT,
                activebackground="#3e3e3e",
                activeforeground="#23c4a4"
            )

    def update_status(self, event=None):
        """Update status bar with cursor position and file info"""
        try:
            cursor_pos = self.message_box.index(tk.INSERT)
            line, col = cursor_pos.split('.')
            file_name = self.current_file[0] if self.current_file[0] else "Untitled"
            file_name = file_name.split('/')[-1]  # Show only filename, not full path
            status_text = f"Line: {line} | Col: {int(col)+1} | {file_name}"
            self.status_bar.config(text=status_text)
        except Exception as e:
            self.status_bar.config(text="Ready")

    def save_file(self, content=None):
        """
        Save the current content to a file.
        
        Args:
            content (str, optional): Content to save. If None, gets content from message_box.
        """
        try:
            if content is None:
                content = self.message_box.get("1.0", "end-1c")
            if self.current_file[0] is None:
                file.save_file_as(self.message_box, self.current_file)
            else:
                with open(self.current_file[0], "w", encoding='utf-8') as file_obj:
                    file_obj.write(content)
            self.status_bar.config(text="File saved successfully")
        except Exception as e:
            self.status_bar.config(text=f"Error saving file: {e}")
