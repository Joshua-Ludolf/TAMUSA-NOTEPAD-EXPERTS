"""
    Group: TAMUSA Notepad Experts (TNE)
    Authors: Joshua Ludolf & Luis Morales
    Class: CSCI 3366 - Programming Languages
"""
import tkinter as tk
from tkinter import filedialog

"""
    This module provides functions to create, open, and save files using a Tkinter-based text editor.
        new_file(message_box, current_file): Clears the content of the message box and resets the current file reference.
        save_file(message_box, current_file): Saves the content of the message box to the specified file.
        save_file_as(message_box, current_file): Prompts the user to save the content of a message box to a file.
        open_file(message_box, current_file): Opens a file dialog to select a file, reads its contents, and displays the contents in the provided message box.
"""

def new_file(message_box, current_file):
    """
    Clears the content of the message box and resets the current file reference.

    Args:
        message_box (tk.Text): The text widget (message box) to be cleared.
        current_file (list): A list containing the current file reference. The first element will be set to None.
    """
    message_box.delete("1.0", "end")
    current_file[0] = None

def save_file(message_box, current_file):
    """
    Saves the content of the message box to the specified file.

    If no file is currently selected, it calls the save_file_as function to prompt the user to select a file.
    Otherwise, it writes the content of the message box to the currently selected file.

    Args:
        message_box (tk.Text): The text widget containing the message to be saved.
        current_file (list): A list where the first element is the path to the current file.

    Raises:
        Exception: If an error occurs during the file writing process, it inserts an error message into the message box.
    """
    if current_file[0] is None:
        save_file_as(message_box, current_file)
    else:
        try:
            message = message_box.get("1.0", "end")
            with open(current_file[0], "w", encoding='utf-8') as file_name:
                file_name.write(message)
        except Exception as e:
            message_box.insert(tk.INSERT, f"Error: {e}")

def save_file_as(message_box, current_file):
    """
    Prompts the user to save the content of a message box to a file.

    Args:
        message_box (tk.Text): The text widget containing the message to be saved.
        current_file (list): A list containing the current file path as its first element.

    Raises:
        Exception: If an error occurs during the file saving process, it will be caught and displayed in the message box.
    """
    try:
        message = message_box.get("1.0", "end")
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"),
                                                            ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file_name:
                file_name.write(message)
            current_file[0] = file_path
    except Exception as e:
        message_box.insert(tk.INSERT, f"Error: {e}")

def open_file(message_box, current_file):
    """
    Opens a file and displays its contents in the message box.

    This function opens a file dialog for the user to select a file, reads the contents
    of the selected file, and displays those contents in the provided message box.

    Args:
        message_box (tk.Text): The text widget where the file contents will be displayed.
        current_file (list): A list where the first element will store the path to the opened file.
    """
    try:
        file_path = filedialog.askopenfilename()
        if file_path:
            current_file[0] = file_path
            with open(file_path, "r", encoding='utf-8') as file:
                message_box.delete("1.0", "end")
                message_box.insert(tk.INSERT, file.read())
    except Exception as e:
        message_box.insert(tk.INSERT, f"Error: {e}")
