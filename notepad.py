"""
    Group: TAMUSA Notepad Experts (TNE)
    Authors: Joshua Ludolf & Luis Morales
    Class: CSCI 3366 - Programming Languages
"""

import tkinter as tk
import file, emoji, fonts, os, pathlib, re
from tkinter import scrolledtext, Menu, ttk, messagebox, Toplevel
from emoji import EmojiPicker



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

    show_emoji_picker(event=None):
        Displays the emoji picker dialog.

    insert_emoji_at_cursor(emoji):
        Inserts the selected emoji at the current cursor position in the text editor.

    create_file_tree():
        Creates a file tree view to navigate through the file system.

    populate_tree(path="."):
        Populates the file tree with directories and files starting from the given path.

    add_directory(parent, path, depth=0):
        Recursively adds directories and files to the file tree view.

    load_more(parent):
        Loads more items in a directory when requested.

    on_tree_double_click(event):
        Handles double-click events on the file tree to open files or expand directories.

    format_size(size):
        Formats the size of a file in a human-readable format (B, KB, MB, etc.).

    update_status(event=None):
        Updates the status bar with the current cursor position and file information.

    save_file(content=None):
        Saves the current content of the text editor to a file.
    """
    def __init__(self, root):
        self.root = root
        self.root.geometry("1920x1080")
        self.root.title("TAMUSA Notepad")
        self.root.configure(bg="#1a1a1a")  # Dark background for the main window
        self.root.font = ("Cascadia Code", 12)  # Modern coding font
        self.root.iconbitmap("tne.ico")
        self.current_file = [None]
        
        # Initialize font manager (will be set after text widget is created)
        self.font_manager = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Create main container frame
        self.main_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Create horizontal paned window
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        # Create and configure the file tree frame
        self.tree_frame = ttk.Frame(self.paned_window)
        self.create_file_tree()
        self.paned_window.add(self.tree_frame, weight=1)

        # Create frame for text editor
        self.editor_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.editor_frame, weight=4)
        
        # Text editor with enhanced styling
        self.message_box = scrolledtext.ScrolledText(
            self.editor_frame,
            font=("Cascadia Code", 12),  # Font as tuple
            wrap=tk.WORD,
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#23c4a4",
            selectbackground="#264f78",
            selectforeground="#ffffff",
            padx=10,
            pady=10
        )
        self.message_box.pack(fill=tk.BOTH, expand=True)

        # Initialize font manager after text widget is created
        self.font_manager = fonts.create_font_manager(self.message_box)

        # Create menu bar after font manager is initialized
        self.create_menu_bar()

        # Create status bar
        self.status_bar = tk.Label(
            self.main_frame,
            text="Ready",
            bg="#2d2d2d",
            fg="#23c4a4",
            font=("Cascadia Code", 10),
            anchor=tk.W,
            padx=10,
            pady=5
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=(0, 5))

        # Bind events for status updates
        self.message_box.bind("<KeyPress>", self.update_status)
        self.message_box.bind("<KeyRelease>", self.update_status)
        
        # Bind emoji shortcuts
        self.message_box.bind("<Control-e>", self.show_emoji_picker)
        self.message_box.bind("<Control-E>", self.show_emoji_picker)
        
        # Bind font shortcuts
        self.message_box.bind("<Control-plus>", lambda e: self.font_manager.increase_font_size())
        self.message_box.bind("<Control-equal>", lambda e: self.font_manager.increase_font_size())  # For keyboards without numpad
        self.message_box.bind("<Control-minus>", lambda e: self.font_manager.decrease_font_size())
        self.message_box.bind("<Control-b>", lambda e: self.font_manager.toggle_bold())
        self.message_box.bind("<Control-i>", lambda e: self.font_manager.toggle_italic())
        self.message_box.bind("<Control-u>", lambda e: self.font_manager.toggle_underline())
        self.message_box.bind("<Control-Shift-F>", lambda e: self.font_manager.show_font_dialog(self.root))

    def show_emoji_picker(self, event=None):
        """Show the emoji picker dialog"""
        EmojiPicker(self.root, self.insert_emoji_at_cursor)
        
    def insert_emoji_at_cursor(self, emoji):
        """Insert emoji at the current cursor position"""
        try:
            cursor_pos = self.message_box.index(tk.INSERT)
            self.message_box.insert(cursor_pos, emoji)
            self.message_box.focus_set()
            # Update status bar
            if hasattr(self, 'status_bar') and self.root.winfo_exists():
                self.status_bar.config(text=f"Inserted emoji: {emoji}")
                # Clear the message after 2 seconds
                self.root.after(2000, lambda: self.status_bar.config(text="Ready") if hasattr(self, 'status_bar') else None)
        except Exception as e:
            print(f"Error inserting emoji: {e}")

    def create_file_tree(self):
        # Style configuration for the tree
        style = ttk.Style()
        style.configure("Treeview",
                       background="#1e1e1e",
                       foreground="#23c4a4",
                       fieldbackground="#1e1e1e")
        style.map('Treeview',
                 background=[('selected', '#264f78')],
                 foreground=[('selected', '#ffffff')])

        # Create tree view
        self.tree = ttk.Treeview(self.tree_frame, selectmode="browse")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add scrollbar
        tree_scroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        # Configure tree columns
        self.tree["columns"] = ("size", "path")  # Added path column
        self.tree.column("#0", width=200, minwidth=150)
        self.tree.column("size", width=100, minwidth=80)
        self.tree.column("path", width=0, stretch=False)  # Hidden column for full path

        # Configure tree headings
        self.tree.heading("#0", text="Name", anchor=tk.W)
        self.tree.heading("size", text="Size", anchor=tk.W)

        # Initialize icons
        self.folder_icon = "📁"
        self.file_icon = "📄"

        # Bind double-click event
        self.tree.bind("<Double-1>", self.on_tree_double_click)

        # Populate tree with Users directory
        self.populate_tree(r"C:\Users")

    def populate_tree(self, path="."):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get absolute path
        abs_path = os.path.abspath(path)
        
        try:
            # Add root directory
            root_node = self.tree.insert("", "end", text=f"{self.folder_icon} {os.path.basename(abs_path)}",
                                       values=("", abs_path))
            self.add_directory(root_node, abs_path)
        except Exception as e:
            self.status_bar.config(text=f"Error accessing directory: {str(e)}")

    def add_directory(self, parent, path, depth=0):
        try:
            # Only go 2 levels deep initially
            if depth > 1:
                # Add a dummy node if we're at max depth
                self.tree.insert(parent, "end", text="...", values=("", ""))
                return

            # Process directories first, then files
            try:
                entries = list(os.scandir(path))
                dirs = sorted([e for e in entries if e.is_dir()], key=lambda e: e.name.lower())
                files = sorted([e for e in entries if e.is_file()], key=lambda e: e.name.lower())
            except PermissionError:
                return

            # Add directories first
            for entry in dirs[:50]:  # Limit to first 50 directories
                try:
                    node = self.tree.insert(parent, "end",
                                          text=f"{self.folder_icon} {entry.name}",
                                          values=("", entry.path))
                    # Recursively add subdirectories
                    self.add_directory(node, entry.path, depth + 1)
                except PermissionError:
                    continue

            # Then add files
            for entry in files[:50]:  # Limit to first 50 files
                try:
                    size = self.format_size(entry.stat().st_size)
                    self.tree.insert(parent, "end",
                                   text=f"{self.file_icon} {entry.name}",
                                   values=(size, entry.path))
                except PermissionError:
                    continue

            # If there are more items, add an indicator
            if len(dirs) > 50 or len(files) > 50:
                remaining = (len(dirs) - 50 if len(dirs) > 50 else 0) + (len(files) - 50 if len(files) > 50 else 0)
                self.tree.insert(parent, "end", text=f"... {remaining} more items", values=("", ""))

        except Exception as e:
            self.status_bar.config(text=f"Error reading directory: {str(e)}")

    def load_more(self, parent):
        """Load more items in a directory when requested"""
        path = self.tree.item(parent)["values"][1]
        if not path:  # Skip if no path stored
            return

        try:
            entries = list(os.scandir(path))
            dirs = sorted([e for e in entries if e.is_dir()], key=lambda e: e.name.lower())
            files = sorted([e for e in entries if e.is_file()], key=lambda e: e.name.lower())

            # Remove existing items
            for child in self.tree.get_children(parent):
                self.tree.delete(child)

            # Add all directories
            for entry in dirs:
                try:
                    node = self.tree.insert(parent, "end",
                                          text=f"{self.folder_icon} {entry.name}",
                                          values=("", entry.path))
                    # Add a dummy node to allow expansion
                    self.tree.insert(node, "end", text="...", values=("", ""))
                except PermissionError:
                    continue

            # Add all files
            for entry in files:
                try:
                    size = self.format_size(entry.stat().st_size)
                    
                    self.tree.insert(parent, "end",
                                   text=f"{self.file_icon} {entry.name}",
                                   values=(size, entry.path))
                except PermissionError:
                    continue

        except Exception as e:
            self.status_bar.config(text=f"Error loading directory contents: {str(e)}")

    def on_tree_double_click(self, event):
        item = self.tree.selection()[0]
        item_text = self.tree.item(item)["text"]
        
        if item_text.startswith(self.file_icon):            # Handle file opening
            full_path = self.tree.item(item)["values"][1]
            self.status_bar.config(text=f"Opening: {full_path}")
            
            try:
                # Try UTF-8 first
                try:
                    with open(full_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                except UnicodeDecodeError:
                    # If UTF-8 fails, try with different encodings
                    encodings = ['latin-1', 'cp1252', 'ascii', 'utf-16']
                    content = None
                    for encoding in encodings:
                        try:
                            with open(full_path, 'r', encoding=encoding) as file:
                                content = file.read()
                            break
                        except UnicodeDecodeError:
                            continue
                    
                    if content is None:
                        # If all text encodings fail, try reading as binary and decode
                        with open(full_path, 'rb') as file:
                            raw_content = file.read()
                            content = raw_content.decode('utf-8', errors='replace')
                
                self.message_box.delete(1.0, tk.END)
                self.message_box.insert(1.0, content)
                self.current_file[0] = full_path
                self.update_status()
            except Exception as e:
                if hasattr(self, 'status_bar') and self.root.winfo_exists():
                    self.status_bar.config(text=f"Error opening file: {str(e)} | Path: {full_path}")
        elif item_text.startswith("..."):
            # If clicking on "... more items", load the full directory
            parent = self.tree.parent(item)
            if parent:
                self.load_more(parent)
        else:
            # Toggle directory expansion
            if self.tree.item(item, "open"):
                self.tree.item(item, open=False)
            else:
                self.tree.item(item, open=True)

    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

    def create_menu_bar(self):
        menu_bar = Menu(
            self.root,
            bg="#2d2d2d",
            fg="#ffffff",
            activebackground="#3e3e3e",
            activeforeground="#23c4a4",
            font=("Cascadia Code", 11),
            relief=tk.FLAT,
            borderwidth=0
        )
        self.root.config(menu=menu_bar)

        # File menu with enhanced styling
        file_menu = Menu(
            menu_bar,
            tearoff=0,
            bg="#2d2d2d",
            fg="#ffffff",
            activebackground="#3e3e3e",
            activeforeground="#23c4a4",
            font=("Cascadia Code", 11),
            relief=tk.FLAT,
            borderwidth=0
        )
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Add menu items with modern styling
        for label, command in [
            ("New", lambda: file.new_file(self.message_box, self.current_file)),
            ("Save", lambda: self.save_file()),
            ("Save As", lambda: file.save_file_as(self.message_box, self.current_file)),
            ("Open", lambda: file.open_file(self.message_box, self.current_file))
        ]:
            file_menu.add_command(
                label=label,
                command=command,
                font=("Cascadia Code", 11),
                compound=tk.LEFT,
                activebackground="#3e3e3e",
                activeforeground="#23c4a4"
            )        # Edit menu with emoji functionality
        edit_menu = Menu(
            menu_bar,
            tearoff=0,
            bg="#2d2d2d",
            fg="#ffffff",
            activebackground="#3e3e3e",
            activeforeground="#23c4a4",
            font=("Cascadia Code", 11),
            relief=tk.FLAT,
            borderwidth=0
        )
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        # Main emoji picker option
        edit_menu.add_command(
            label="Insert Emoji... (Ctrl+E)",
            command=self.show_emoji_picker,
            font=("Cascadia Code", 11),
            activebackground="#3e3e3e",
            activeforeground="#23c4a4"
        )
        
        edit_menu.add_separator()
        
        # Quick access emoji submenu
        emoji_submenu = Menu(
            edit_menu,
            tearoff=0,
            bg="#2d2d2d",
            fg="#ffffff",
            activebackground="#3e3e3e",
            activeforeground="#23c4a4",
            font=("Cascadia Code", 11),
            relief=tk.FLAT,
            borderwidth=0
        )
        edit_menu.add_cascade(label="Quick Emojis", menu=emoji_submenu)
        
        # Add common emoji shortcuts to submenu
        common_emojis = [
            ("😀 Grinning Face", "😀"),
            ("😂 Face with Tears of Joy", "😂"),
            ("❤️ Red Heart", "❤️"),
            ("👍 Thumbs Up", "👍"),
            ("🎉 Party Popper", "🎉"),
            ("🔥 Fire", "🔥"),
            ("✨ Sparkles", "✨"),
            ("🚀 Rocket", "🚀")
        ]
        
        for label, emoji in common_emojis:
            emoji_submenu.add_command(
                label=label,
                command=lambda e=emoji: self.insert_emoji_at_cursor(e),
                font=("Cascadia Code", 11),
                activebackground="#3e3e3e",
                activeforeground="#23c4a4"            )

        # Format menu with font functionality
        format_menu = Menu(
            menu_bar,
            tearoff=0,
            bg="#2d2d2d",
            fg="#ffffff",
            activebackground="#3e3e3e",
            activeforeground="#23c4a4",
            font=("Cascadia Code", 11),
            relief=tk.FLAT,
            borderwidth=0
        )
        menu_bar.add_cascade(label="Format", menu=format_menu)
        
        # Font dialog option
        format_menu.add_command(
            label="Font... (Ctrl+Shift+F)",
            command=lambda: self.font_manager.show_font_dialog(self.root),
            font=("Cascadia Code", 11),
            activebackground="#3e3e3e",
            activeforeground="#23c4a4"
        )
        
        format_menu.add_separator()
        
        # Font size controls
        format_menu.add_command(
            label="Increase Font Size (Ctrl++)",
            command=self.font_manager.increase_font_size,
            font=("Cascadia Code", 11),
            activebackground="#3e3e3e",
            activeforeground="#23c4a4"
        )
        
        format_menu.add_command(
            label="Decrease Font Size (Ctrl+-)",
            command=self.font_manager.decrease_font_size,
            font=("Cascadia Code", 11),
            activebackground="#3e3e3e",
            activeforeground="#23c4a4"
        )
        
        format_menu.add_separator()
        
        # Font style toggles
        format_menu.add_command(
            label="Toggle Bold (Ctrl+B)",
            command=self.font_manager.toggle_bold,
            font=("Cascadia Code", 11),
            activebackground="#3e3e3e",
            activeforeground="#23c4a4"
        )
        
        format_menu.add_command(
            label="Toggle Italic (Ctrl+I)",
            command=self.font_manager.toggle_italic,
            font=("Cascadia Code", 11),
            activebackground="#3e3e3e",
            activeforeground="#23c4a4"
        )
        
        format_menu.add_command(
            label="Toggle Underline (Ctrl+U)",
            command=self.font_manager.toggle_underline,
            font=("Cascadia Code", 11),
            activebackground="#3e3e3e",
            activeforeground="#23c4a4"
        )
        
        format_menu.add_command(
            label="Toggle Strikethrough",
            command=self.font_manager.toggle_strikethrough,
            font=("Cascadia Code", 11),
            activebackground="#3e3e3e",
            activeforeground="#23c4a4"
        )
        
        format_menu.add_separator()
        
        # Color options
        format_menu.add_command(
            label="Text Color...",
            command=self.font_manager.change_text_color,
            font=("Cascadia Code", 11),
            activebackground="#3e3e3e",
            activeforeground="#23c4a4"
        )
        
        format_menu.add_command(
            label="Background Color...",
            command=self.font_manager.change_background_color,
            font=("Cascadia Code", 11),
            activebackground="#3e3e3e",
            activeforeground="#23c4a4"
        )
        
        format_menu.add_separator()
        
        # Reset option  
        format_menu.add_command(
            label="Reset to Default",
            command=self.font_manager.reset_to_default,
            font=("Cascadia Code", 11),
            activebackground="#3e3e3e",
            activeforeground="#23c4a4"
        )

    def update_status(self, event=None):
        """Update status bar with cursor position and file info"""
        try:
            cursor_pos = self.message_box.index(tk.INSERT)
            line, col = cursor_pos.split('.')
            file_name = self.current_file[0] if self.current_file[0] else "Untitled"
            file_name = file_name.split('/')[-1]  # Show only filename, not full path
            status_text = f"Line: {line} | Col: {int(col)+1} | {file_name}"
            if hasattr(self, 'status_bar') and self.root.winfo_exists():
                self.status_bar.config(text=status_text)
        except tk.TclError:
            # Widget has been destroyed
            pass
        except Exception as e:
            if hasattr(self, 'status_bar') and self.root.winfo_exists():
                self.status_bar.config(text="Ready")

    def save_file(self, content=None):
        """
        Save the current content to a file.
        
        Args:
            content (str, optional): Content to save. If None, gets content from message_box.
        """
        try:
            if content is None:
                content = self.message_box.get("1.0", "end-1c")
            if self.current_file[0] is None:
                file.save_file_as(self.message_box, self.current_file)
            else:
                with open(self.current_file[0], "w", encoding='utf-8') as file_obj:
                    file_obj.write(content)
            # Only update status bar if the widget still exists
            if hasattr(self, 'status_bar') and self.root.winfo_exists():
                self.status_bar.config(text="File saved successfully")
        except tk.TclError:
            # Widget has been destroyed, ignore
            pass
        except Exception as e:
            if hasattr(self, 'status_bar') and self.root.winfo_exists():
                self.status_bar.config(text=f"Error saving file: {e}")
