"""
    Group: TAMUSA Notepad Experts (TNE)
    Authors: Joshua Ludolf & Luis Morales
    Class: CSCI 3366 - Programming Languages
"""

import tkinter as tk
from tkinter import scrolledtext, Menu, ttk
import file
import os
import pathlib
import re

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
    """
    def __init__(self, root):
        self.root = root
        self.root.geometry("1920x1080")
        self.root.title("TAMUSA Notepad")
        self.root.configure(bg="#1a1a1a")  # Dark background for the main window
        self.root.font = ("Cascadia Code", 12)  # Modern coding font
        self.root.iconbitmap("tne.ico")
        self.current_file = [None]
        self.create_widgets()

    def create_widgets(self):
        # Create main container frame
        self.main_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.create_menu_bar()

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
        
        if item_text.startswith(self.file_icon):
            # Handle file opening
            full_path = self.tree.item(item)["values"][1]
            self.status_bar.config(text=f"Opening: {full_path}")
            
            try:
                with open(full_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.message_box.delete(1.0, tk.END)
                    self.message_box.insert(1.0, content)
                    self.current_file[0] = full_path
                    self.update_status()
            except Exception as e:
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
            )

    def update_status(self, event=None):
        """Update status bar with cursor position and file info"""
        try:
            cursor_pos = self.message_box.index(tk.INSERT)
            line, col = cursor_pos.split('.')
            file_name = self.current_file[0] if self.current_file[0] else "Untitled"
            file_name = file_name.split('/')[-1]  # Show only filename, not full path
            status_text = f"Line: {line} | Col: {int(col)+1} | {file_name}"
            self.status_bar.config(text=status_text)
        except Exception as e:
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
            self.status_bar.config(text="File saved successfully")
        except Exception as e:
            self.status_bar.config(text=f"Error saving file: {e}")
