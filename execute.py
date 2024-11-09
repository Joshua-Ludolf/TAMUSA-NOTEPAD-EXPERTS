"""
    Group: TAMUSA Notepad Experts (TNE)
    Authors: Joshua Ludolf & Luis Morales
    Class: CSCI 3366 - Programming Languages
"""
import tkinter as tk
from notepad import NotePad

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
    root.mainloop()

if __name__ == "__main__":
    main()