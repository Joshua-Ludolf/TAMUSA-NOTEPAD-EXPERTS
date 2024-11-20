"""
    Group: TAMUSA Notepad Experts (TNE)
    Authors: Joshua Ludolf & Luis Morales
    Class: CSCI 3366 - Programming Languages
"""
import tkinter as tk
from notepad import NotePad
import atexit

# Global variables
app = None
is_running = True
last_content = ""  # Store the last known content

def save_notes():
    """Save notes if there's an active file"""
    global app, last_content
    try:
        if app and hasattr(app, 'current_file') and app.current_file[0]:
            app.save_file(last_content)
    except Exception as e:
        print(f"Error during auto-save: {str(e)}")

def update_content():
    """Update the last known content"""
    global app, last_content
    try:
        if app and hasattr(app, 'message_box'):
            last_content = app.message_box.get('1.0', tk.END)
    except Exception:
        pass  # Ignore errors during content update

def cleanup():
    """Handle cleanup when the application exits"""
    global app, is_running
    is_running = False
    try:
        save_notes()
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")

def on_closing(root):
    """Handle window closing event"""
    global is_running
    is_running = False
    update_content()  # Capture the final content
    save_notes()
    root.destroy()

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
    global app, is_running
    root = tk.Tk()
    root.configure(bg="#1e1e1e")
    app = NotePad(root)

    def auto_save():
        """Recursive function to handle auto-saving"""
        if is_running:
            try:
                update_content()  # Update content before saving
                save_notes()
                if is_running:  # Check again in case status changed during save
                    root.after(1000, auto_save)
            except Exception as e:
                print(f"Error in auto-save: {str(e)}")

    # Start the auto-save cycle
    auto_save()

    # Register cleanup handlers
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    atexit.register(cleanup)

    try:
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
        update_content()  # Capture content before handling error
        save_notes()

if __name__ == "__main__":
    main()