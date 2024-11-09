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
        self.root.font = ("Helvetica", 12)
        self.current_file = [None]  # List to hold current file path
        self.create_widgets()

    def create_widgets(self):
        self.create_menu_bar()
        self.message_box = scrolledtext.ScrolledText(self.root, font=("Helvetica", 12), width=165, height=40, wrap=tk.WORD)
        self.message_box.configure(bg="#1e1e1e", fg="#f5f5f5", insertbackground="#f5f5f5", selectbackground="#5c5c5c", font=("Helvetica", 12))
        self.message_box.grid(row=1, column=0, columnspan=3, rowspan=3, padx=10, pady=10)

    def create_menu_bar(self):
        menu_bar = Menu(self.root, bg="#2e2e2e", fg="#ffffff", activebackground="#3e3e3e", activeforeground="#23c4a4", font=("Helvetica", 12))
        self.root.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0, bg="#2e2e2e", fg="#23c4a4", activebackground="#3e3e3e", activeforeground="#ffffff")
        menu_bar.add_cascade(label="File", menu=file_menu, font=("Helvetica", 12))
        file_menu.add_command(label="New", command=lambda: file.new_file(self.message_box, self.current_file), font=("Helvetica", 12))
        file_menu.add_command(label="Save", command=lambda: file.save_file(self.message_box, self.current_file), font=("Helvetica", 12))
        file_menu.add_command(label="Save As", command=lambda: file.save_file_as(self.message_box, self.current_file), font=("Helvetica", 12))
        file_menu.add_command(label="Open", command=lambda: file.open_file(self.message_box, self.current_file), font=("Helvetica", 12))


