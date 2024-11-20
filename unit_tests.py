import unittest
import tkinter as tk

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from notepad import NotePad
import file

class TestNotepad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n=== TAMUSA Notepad Testing Suite ===\n")

    def setUp(self):
        self.root = tk.Tk()
        self.notepad = NotePad(self.root)
        self.test_file = "test_document.txt"
        print(f"\nRunning: {self._testMethodName}")
        print("-" * 40)
    
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.root.destroy()
        print("-" * 40)

    def test_new_file(self):
        print("Testing new file creation...")
        # Add some text
        test_content = "Test content"
        self.notepad.message_box.insert("1.0", test_content)
        print(f"Added content: '{test_content}'")
        
        # Create new file
        file.new_file(self.notepad.message_box, self.notepad.current_file)
        print("Created new file")
        
        # Verify content is cleared
        content = self.notepad.message_box.get("1.0", tk.END).strip()
        print(f"Content after new file: '{content}'")
        self.assertEqual(content, "")
        self.assertIsNone(self.notepad.current_file[0])
        print("✓ New file test passed")

    def test_save_and_open_file(self):
        print("Testing save and open operations...")
        test_content = "Hello, World!"
        self.notepad.message_box.insert("1.0", test_content)
        print(f"Initial content: '{test_content}'")
        
        # Save file
        self.notepad.current_file[0] = self.test_file
        file.save_file(self.notepad.message_box, self.notepad.current_file)
        print(f"Saved to file: {self.test_file}")
        
        # Clear content
        self.notepad.message_box.delete("1.0", tk.END)
        print("Cleared content")
        
        # Open file and verify content
        file.open_file(self.notepad.message_box, self.notepad.current_file)
        content = self.notepad.message_box.get("1.0", tk.END).strip()
        print(f"Content after reload: '{content}'")
        self.assertEqual(content, test_content)
        print("✓ Save and open test passed")
    
    def test_ui_elements(self):
        print("Testing UI elements...")
        # Test window properties
        self.assertEqual(self.root.title(), "TAMUSA Notepad")
        print("✓ Window title verified")
        
        # Test text area properties
        text_widget = self.notepad.message_box
        self.assertEqual(text_widget.cget("bg"), "#1e1e1e")
        self.assertEqual(text_widget.cget("fg"), "#f5f5f5")
        self.assertEqual(text_widget.cget("font"), "Helvetica 12")
        print("✓ Text widget properties verified")
        
        # Test menu existence
        menu_bar = self.root.nametowidget(self.root.cget("menu"))
        self.assertIsInstance(menu_bar, tk.Menu)
        print("✓ Menu bar verified")

    def test_large_content(self):
        print("Testing large content handling...")
        # Test with large content
        large_content = "Test line\n" * 1000
        self.notepad.message_box.insert("1.0", large_content)
        print(f"Added {large_content.count('\n')} lines")
        
        # Save large content
        self.notepad.current_file[0] = self.test_file
        file.save_file(self.notepad.message_box, self.notepad.current_file)
        print("Saved large content")
        
        # Clear and reload
        self.notepad.message_box.delete("1.0", tk.END)
        file.open_file(self.notepad.message_box, self.notepad.current_file)
        print("Reloaded content")
        
        # Verify content length
        content = self.notepad.message_box.get("1.0", tk.END)
        line_count = content.count('\n')
        print(f"Line count after reload: {line_count}")
        self.assertGreaterEqual(content.count('\n'), 1000)
        self.assertLess(content.count('\n'), 1003)
        print("✓ Large content test passed")
        
    def test_special_characters(self):
        print("Testing special character handling...")
        # Test with basic ASCII
        special_content = "Hello World"
        self.notepad.message_box.insert("1.0", special_content)
        print(f"Testing basic ASCII: '{special_content}'")
        
        # Save and reload
        self.notepad.current_file[0] = self.test_file
        file.save_file(self.notepad.message_box, self.notepad.current_file)
        print("Saved ASCII content")
        
        # Clear and reload
        self.notepad.message_box.delete("1.0", tk.END)
        file.open_file(self.notepad.message_box, self.notepad.current_file)
        print("Reloaded ASCII content")
        
        # Verify basic content
        content = self.notepad.message_box.get("1.0", tk.END).strip()
        print(f"Content after reload: '{content}'")
        self.assertEqual(content, special_content)
        print("✓ Basic ASCII test passed")
        
        # Test with special characters
        special_content = "Special chars: ABC 123"
        print(f"\nTesting special chars: '{special_content}'")
        self.notepad.message_box.delete("1.0", tk.END)
        self.notepad.message_box.insert("1.0", special_content)
        
        file.save_file(self.notepad.message_box, self.notepad.current_file)
        print("Saved special content")
        
        # Clear and reload
        self.notepad.message_box.delete("1.0", tk.END)
        file.open_file(self.notepad.message_box, self.notepad.current_file)
        print("Reloaded special content")
        
        # Verify special content
        content = self.notepad.message_box.get("1.0", tk.END).strip()
        print(f"Content after reload: '{content}'")
        self.assertEqual(content, special_content)
        print("✓ Special characters test passed")

if __name__ == '__main__':
    unittest.main(verbosity=2)