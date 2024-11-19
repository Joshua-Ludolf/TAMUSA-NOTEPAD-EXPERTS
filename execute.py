"""
    Group: TAMUSA Notepad Experts (TNE)
    Authors: Joshua Ludolf & Luis Morales
    Class: CSCI 3366 - Programming Languages
"""
import tkinter as tk
from notepad import NotePad
import atexit

def save_notes():
    # Logic to save the notes
    app.save()  # Assuming the NotePad class has a save method

# Register the save_notes function to be called on exit
atexit.register(save_notes)

def main():
    """
    Main function to initialize and run the NotePad application.

    This function creates the main application window, configures its background color,
    and starts the Tkinter main event loop.

    Parameters:
        None

    Returns:
        None
    """
    root = tk.Tk()
    root.configure(bg="#1e1e1e")
    app = NotePad(root)

    # Automatically save notes every 60 seconds
    root.after(60000, save_notes)  # Save every 60 seconds

    try:
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
        save_notes()  # Save notes in case of an error

if __name__ == "__main__":
    main()