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

def save_file(message_box, current_file, content=None):
    """
    Saves the content of the message box to the specified file.

    Args:
        message_box (tk.Text): The text widget containing the message to be saved.
        current_file (list): A list where the first element is the path to the current file.
        content (str): The content to be saved. If None, the content of the message box will be used.

    Returns:
        bool: True if the file was saved successfully, False otherwise.
    """
    try:
        if content is None:
            content = message_box.get("1.0", "end-1c")
        with open(current_file[0], 'w', encoding='utf-8', newline='') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

def save_file_as(message_box, current_file, target_path=None):
    """
    Save the current file as a new file

    Args:
        message_box (tk.Text): The text widget containing the message to be saved.
        current_file (list): A list containing the current file path as its first element.
        target_path (str): The path to save the file. If None, a file dialog will be opened.

    Returns:
        bool: True if the file was saved successfully, False otherwise.
    """
    try:
        if target_path is None:
            target_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if target_path:
            current_file[0] = target_path
            content = message_box.get("1.0", "end-1c")
            with open(target_path, 'w', encoding='utf-8', newline='') as f:
                f.write(content)
            return True
    except Exception as e:
        print(f"Error saving file: {e}")
    return False

def open_file(message_box, current_file, file_path=None):
    """
    Open a file and load its contents into the text box

    Args:
        message_box (tk.Text): The text widget where the file contents will be displayed.
        current_file (list): A list where the first element will store the path to the opened file.
        file_path (str): The path to the file to be opened. If None, a file dialog will be opened.

    Returns:
        bool: True if the file was opened successfully, False otherwise.
    """
    try:
        if file_path is None:
            file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            current_file[0] = file_path
            with open(file_path, 'r', encoding='utf-8', newline='') as f:
                content = f.read()
            message_box.delete("1.0", tk.END)
            message_box.insert("1.0", content)
            return True
    except Exception as e:
        print(f"Error opening file: {e}")
    return False
