"""
Test script to verify emoji functionality
"""
import tkinter as tk
from notepad import EmojiPicker

def test_emoji_insertion(emoji):
    print(f"Selected emoji: {emoji}")

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Test the emoji picker
    picker = EmojiPicker(root, test_emoji_insertion)
    root.wait_window(picker.window)
    
    root.destroy()

if __name__ == "__main__":
    main()
