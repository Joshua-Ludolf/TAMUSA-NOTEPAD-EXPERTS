"""
    Group: TAMUSA Notepad Experts (TNE)
    Authors: Joshua Ludolf & Luis Morales
    Class: CSCI 3366 - Programming Languages
"""
import tkinter as tk
from tkinter import filedialog

def new_file(message_box, current_file):
    message_box.delete("1.0", "end")
    current_file[0] = None

def save_file(message_box, current_file):
    if current_file[0] is None:
        save_file_as(message_box, current_file)
    else:
        try:
            message = message_box.get("1.0", "end")
            with open(current_file[0], "w") as file_name:
                file_name.write(message)
        except Exception as e:
            message_box.insert(tk.INSERT, f"Error: {e}")

def save_file_as(message_box, current_file):
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
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"),
                                                          ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as in_file:
                msg = in_file.read()
                message_box.delete("1.0", "end")
                message_box.insert(tk.INSERT, msg)
            current_file[0] = file_path
    except FileNotFoundError:
        message_box.insert(tk.INSERT, "File was not found! Please provide an existing file.")
