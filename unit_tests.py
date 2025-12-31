import unittest
import tkinter as tk
from tkinter import font as tkfont
import sys
import os
import tempfile
import random
import string
import io

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from notepad import NotePad
import file

class TestNotepad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n=== TAMUSA Notepad Testing Suite ===\n")
        # Create a temporary directory for test files
        cls.test_dir = tempfile.mkdtemp(prefix="notepad_test_")
        print(f"Test directory: {cls.test_dir}")

    @classmethod
    def tearDownClass(cls):
        # Clean up the temporary directory
        try:
            for root, dirs, files in os.walk(cls.test_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(cls.test_dir)
            print(f"\nCleaned up test directory: {cls.test_dir}")
        except Exception as e:
            print(f"Warning: Could not clean up test directory: {e}")

    def generate_test_file_path(self, prefix="test", suffix=".txt"):
        """Generate a unique test file path"""
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        return os.path.join(self.test_dir, f"{prefix}_{random_str}{suffix}")

    def setUp(self):
        self.root = tk.Tk()
        self.notepad = NotePad(self.root)
        self.test_file = self.generate_test_file_path()
        print(f"\nRunning: {self._testMethodName}")
        print(f"Using test file: {self.test_file}")
        print("-" * 40)
    
    def tearDown(self):
        try:
            if os.path.exists(self.test_file):
                os.remove(self.test_file)
            self.root.destroy()
        except Exception as e:
            print(f"Warning: Cleanup failed: {e}")
        print("-" * 40)

    def test_new_file(self):
        """Test creating a new file"""
        print("Testing new file creation...")
        # Test with different content types
        test_contents = [
            "Simple text",
            "Multi\nline\ntext",
            "Special chars: !@#$%^&*()",
            "Unicode: 你好, Привет, مرحبا"
        ]
        
        for test_content in test_contents:
            with self.subTest(content=test_content):
                # Add content
                self.notepad.message_box.insert("1.0", test_content)
                print(f"Added content: '{test_content}'")
                
                # Create new file
                file.new_file(self.notepad.message_box, self.notepad.current_file)
                print("Created new file")
                
                # Verify content is cleared
                content = self.notepad.message_box.get("1.0", tk.END).strip()
                self.assertEqual(content, "")
                self.assertIsNone(self.notepad.current_file[0])
                print("✓ New file test passed for current content")

    def test_save_and_open_file(self):
        """Test saving and opening files with different content types"""
        print("Testing save and open operations...")
        test_cases = [
            ("plain.txt", "Hello, World!"),
            ("multiline.txt", "Line 1\nLine 2\nLine 3"),
            ("special.txt", "Special: !@#$%^&*()"),
            ("unicode.txt", "Unicode: 你好, Привет, مرحبا"),
            ("large.txt", "Test line\n" * 100)
        ]
        
        for filename_suffix, test_content in test_cases:
            with self.subTest(file=filename_suffix, content=test_content):
                test_file = self.generate_test_file_path(suffix=f"_{filename_suffix}")
                print(f"Testing with file: {test_file}")
                print(f"Content: '{test_content[:50]}...' ({len(test_content)} chars)")
                
                # Write content directly to file
                with open(test_file, 'w', encoding='utf-8', newline='') as f:
                    f.write(test_content)
                self.notepad.current_file[0] = test_file
                
                # Open file and verify
                file.open_file(self.notepad.message_box, self.notepad.current_file, test_file)
                content = self.notepad.message_box.get("1.0", "end-1c")
                self.assertEqual(content.strip(), test_content.strip())
                print("✓ Save and open test passed")
                
                # Cleanup
                if os.path.exists(test_file):
                    os.remove(test_file)

    def test_ui_elements(self):
        """Test UI elements and their properties"""
        print("Testing UI elements...")
        
        # Test window title
        self.assertEqual(self.root.title(), "TAMUSA Notepad")
        print("✓ Window title verified")
        
        # Test text widget font
        text_widget = self.notepad.message_box
        font_str = text_widget.cget("font")
        # Tk may return a named font (e.g., "font1"); resolve to actual family/size.
        resolved = tkfont.Font(root=self.root, font=font_str)
        self.assertEqual(int(resolved.cget("size")), 12)
        self.assertTrue(any(name in str(resolved.cget("family")) for name in [
            "Cascadia Code",
            "DejaVu",
            "Liberation",
            "Noto",
            "TkFixedFont",
            "Courier",
        ]))
        print("✓ Text widget properties verified")
        
        # Test menu existence and properties
        menu_bar = self.root.nametowidget(self.root.cget("menu"))
        self.assertIsInstance(menu_bar, tk.Menu)
        print("✓ Menu bar verified")

    def test_large_file_handling(self):
        """Test handling of large files with different sizes"""
        print("Testing large file handling...")
        test_file = self.generate_test_file_path(suffix=".txt")
        sizes = [100, 1000, 5000]
        
        for size in sizes:
            with self.subTest(size=size):
                # Generate content with explicit line numbering
                content = "\n".join([f"Line {i+1}" for i in range(size)])  
                print(f"Testing with {size} lines...")
                
                # Write content directly to file
                with open(test_file, 'w', encoding='utf-8', newline='') as f:
                    f.write(content)
                print(f"Saved file of {size} lines")
                
                # Load file and verify content
                self.notepad.current_file[0] = test_file
                file.open_file(self.notepad.message_box, self.notepad.current_file, test_file)
                loaded_content = self.notepad.message_box.get("1.0", "end-1c")
                self.assertEqual(loaded_content, content)
                self.assertEqual(loaded_content.count('\n'), size - 1)  
                print(f"✓ Large file test passed for {size} lines")
                
                # Cleanup
                if os.path.exists(test_file):
                    os.remove(test_file)

    def test_special_content(self):
        """Test handling of special content types"""
        print("Testing special content handling...")
        test_file = self.generate_test_file_path(suffix=".txt")
        test_cases = {
            'empty': '',
            'spaces': '   ',
            'newlines': '\n\n\n',
            'unicode': '你好, Привет, مرحبا, 안녕하세요',
            'symbols': '!@#$%^&*()_+-=[]{}\\|;:\'",.<>/?`~',
            'mixed': 'Hello\n   World\n你好\n!@#$'
        }
        
        for case, content in test_cases.items():
            with self.subTest(case=case):
                print(f"\nTesting {case} content...")
                
                # Write content directly to file
                with open(test_file, 'w', encoding='utf-8', newline='') as f:
                    f.write(content)
                
                # Load file and verify content
                self.notepad.current_file[0] = test_file
                file.open_file(self.notepad.message_box, self.notepad.current_file, test_file)
                loaded_content = self.notepad.message_box.get("1.0", "end-1c")
                self.assertEqual(loaded_content, content)
                print(f"✓ {case} content test passed")
                
                # Cleanup
                if os.path.exists(test_file):
                    os.remove(test_file)

if __name__ == '__main__':
    unittest.main(verbosity=2)