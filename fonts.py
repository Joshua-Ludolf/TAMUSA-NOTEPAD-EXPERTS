"""
    Group: TAMUSA Notepad Experts (TNE)
    Authors: Joshua Ludolf & Luis Morales
    Class: CSCI 3366 - Programming Languages
    
    Font management module for the TAMUSA Notepad application.
    Provides functionality to change font family, size, style, and other text formatting options.
"""

import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, font
import json
import os


def preferred_mono_font_family(root=None):
    """Return a reasonable monospace font family available on this system."""
    candidates = [
        "Cascadia Code",  # Windows / dev machines
        "DejaVu Sans Mono",  # common on Linux/Alpine
        "Liberation Mono",
        "Noto Sans Mono",
        "Courier New",
        "TkFixedFont",  # Tk fallback
    ]

    try:
        available = set(font.families(root) if root is not None else font.families())
    except Exception:
        return "TkFixedFont"

    for family in candidates:
        if family in available:
            return family
    return "TkFixedFont"


class FontManager:
    """
    A class to manage font settings for the text editor.
    
    Attributes:
        text_widget: The text widget to apply font changes to
        current_font: Dictionary containing current font settings
        config_file: Path to the font configuration file
    """
    
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.config_file = "font_config.json"

        try:
            root = self.text_widget.winfo_toplevel()
        except Exception:
            root = None

        default_family = preferred_mono_font_family(root)
        
        # Default font settings
        self.current_font = {
            'family': default_family,
            'size': 12,
            'weight': 'normal',  # normal, bold
            'slant': 'roman',    # roman, italic
            'underline': 0,
            'overstrike': 0,
            'foreground': '#d4d4d4',
            'background': '#1e1e1e'
        }
        
        # Load saved font settings
        self.load_font_config()
        
        # Apply current font settings
        self.apply_font()
    
    def load_font_config(self):
        """Load font configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    saved_config = json.load(f)
                    self.current_font.update(saved_config)

            # If the saved font family isn't available on this platform, fall back.
            try:
                root = self.text_widget.winfo_toplevel()
            except Exception:
                root = None
            if self.current_font.get('family') not in set(font.families(root)):
                self.current_font['family'] = preferred_mono_font_family(root)
        except Exception as e:
            print(f"Error loading font config: {e}")
    
    def save_font_config(self):
        """Save current font configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.current_font, f, indent=2)
        except Exception as e:
            print(f"Error saving font config: {e}")
    
    def apply_font(self):
        """Apply current font settings to the text widget"""
        try:
            # Create font tuple
            font_tuple = (
                self.current_font['family'],
                self.current_font['size'],
                self.current_font['weight'],
                self.current_font['slant']
            )
            
            # Configure text widget
            self.text_widget.configure(
                font=font_tuple,
                fg=self.current_font['foreground'],
                bg=self.current_font['background']
            )
            
            # Apply additional formatting
            current_font_obj = font.Font(
                family=self.current_font['family'],
                size=self.current_font['size'],
                weight=self.current_font['weight'],
                slant=self.current_font['slant'],
                underline=self.current_font['underline'],
                overstrike=self.current_font['overstrike']
            )
            
            self.text_widget.configure(font=current_font_obj)
            
        except Exception as e:
            print(f"Error applying font: {e}")
    
    def get_available_fonts(self):
        """Get list of available system fonts"""
        return sorted(font.families())
    
    def show_font_dialog(self, parent=None):
        """Show comprehensive font selection dialog"""
        FontDialog(parent or self.text_widget.master, self)
    
    def change_font_family(self, family):
        """Change font family"""
        self.current_font['family'] = family
        self.apply_font()
        self.save_font_config()
    
    def change_font_size(self, size):
        """Change font size"""
        try:
            size = int(size)
            if 6 <= size <= 72:
                self.current_font['size'] = size
                self.apply_font()
                self.save_font_config()
            else:
                messagebox.showwarning("Invalid Size", "Font size must be between 6 and 72")
        except ValueError:
            messagebox.showerror("Invalid Size", "Please enter a valid number")
    
    def toggle_bold(self):
        """Toggle bold formatting"""
        self.current_font['weight'] = 'bold' if self.current_font['weight'] == 'normal' else 'normal'
        self.apply_font()
        self.save_font_config()
    
    def toggle_italic(self):
        """Toggle italic formatting"""
        self.current_font['slant'] = 'italic' if self.current_font['slant'] == 'roman' else 'roman'
        self.apply_font()
        self.save_font_config()
    
    def toggle_underline(self):
        """Toggle underline formatting"""
        self.current_font['underline'] = 1 if self.current_font['underline'] == 0 else 0
        self.apply_font()
        self.save_font_config()
    
    def toggle_strikethrough(self):
        """Toggle strikethrough formatting"""
        self.current_font['overstrike'] = 1 if self.current_font['overstrike'] == 0 else 0
        self.apply_font()
        self.save_font_config()
    
    def change_text_color(self):
        """Change text color"""
        color = colorchooser.askcolor(initialcolor=self.current_font['foreground'])
        if color[1]:  # color[1] is the hex value
            self.current_font['foreground'] = color[1]
            self.apply_font()
            self.save_font_config()
    
    def change_background_color(self):
        """Change background color"""
        color = colorchooser.askcolor(initialcolor=self.current_font['background'])
        if color[1]:  # color[1] is the hex value
            self.current_font['background'] = color[1]
            self.apply_font()
            self.save_font_config()
    
    def reset_to_default(self):
        """Reset font settings to default"""
        try:
            root = self.text_widget.winfo_toplevel()
        except Exception:
            root = None
        default_family = preferred_mono_font_family(root)
        self.current_font = {
            'family': default_family,
            'size': 12,
            'weight': 'normal',
            'slant': 'roman',
            'underline': 0,
            'overstrike': 0,
            'foreground': '#d4d4d4',
            'background': '#1e1e1e'
        }
        self.apply_font()
        self.save_font_config()
    
    def increase_font_size(self):
        """Increase font size by 1"""
        if self.current_font['size'] < 72:
            self.current_font['size'] += 1
            self.apply_font()
            self.save_font_config()
    
    def decrease_font_size(self):
        """Decrease font size by 1"""
        if self.current_font['size'] > 6:
            self.current_font['size'] -= 1
            self.apply_font()
            self.save_font_config()


class FontDialog:
    """
    Font selection dialog window
    """
    
    def __init__(self, parent, font_manager):
        self.parent = parent
        self.font_manager = font_manager
        self.create_dialog()
    
    def create_dialog(self):
        """Create the font dialog window"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Font Settings")
        self.dialog.geometry("600x500")
        self.dialog.configure(bg="#1a1a1a")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        self.create_widgets()
    
    def center_dialog(self):
        """Center the dialog on the parent window"""
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.dialog.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Main frame
        main_frame = tk.Frame(self.dialog, bg="#1a1a1a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Font Family Section
        family_frame = tk.LabelFrame(main_frame, text="Font Family", bg="#1a1a1a", fg="#23c4a4", 
                                   font=("Cascadia Code", 12, "bold"))
        family_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Font family listbox with scrollbar
        family_list_frame = tk.Frame(family_frame, bg="#1a1a1a")
        family_list_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.family_listbox = tk.Listbox(family_list_frame, height=8, bg="#2d2d2d", fg="#ffffff",
                                       selectbackground="#264f78", font=("Cascadia Code", 10))
        family_scrollbar = tk.Scrollbar(family_list_frame, orient=tk.VERTICAL)
        
        self.family_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        family_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.family_listbox.config(yscrollcommand=family_scrollbar.set)
        family_scrollbar.config(command=self.family_listbox.yview)
        
        # Populate font families
        fonts = self.font_manager.get_available_fonts()
        for font_family in fonts:
            self.family_listbox.insert(tk.END, font_family)
        
        # Select current font
        try:
            current_index = fonts.index(self.font_manager.current_font['family'])
            self.family_listbox.selection_set(current_index)
            self.family_listbox.see(current_index)
        except ValueError:
            pass
        
        # Font Size Section
        size_frame = tk.LabelFrame(main_frame, text="Font Size", bg="#1a1a1a", fg="#23c4a4",
                                 font=("Cascadia Code", 12, "bold"))
        size_frame.pack(fill=tk.X, pady=(0, 15))
        
        size_control_frame = tk.Frame(size_frame, bg="#1a1a1a")
        size_control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Size spinbox
        tk.Label(size_control_frame, text="Size:", bg="#1a1a1a", fg="#ffffff",
                font=("Cascadia Code", 10)).pack(side=tk.LEFT)
        
        self.size_var = tk.StringVar(value=str(self.font_manager.current_font['size']))
        self.size_spinbox = tk.Spinbox(size_control_frame, from_=6, to=72, width=10,
                                     textvariable=self.size_var, bg="#2d2d2d", fg="#ffffff",
                                     font=("Cascadia Code", 10))
        self.size_spinbox.pack(side=tk.LEFT, padx=(10, 20))
        
        # Quick size buttons
        quick_sizes = [8, 10, 12, 14, 16, 18, 24, 36]
        for size in quick_sizes:
            btn = tk.Button(size_control_frame, text=str(size), width=3,
                          command=lambda s=size: self.set_quick_size(s),
                          bg="#2d2d2d", fg="#ffffff", font=("Cascadia Code", 9))
            btn.pack(side=tk.LEFT, padx=2)
        
        # Font Style Section
        style_frame = tk.LabelFrame(main_frame, text="Font Style", bg="#1a1a1a", fg="#23c4a4",
                                  font=("Cascadia Code", 12, "bold"))
        style_frame.pack(fill=tk.X, pady=(0, 15))
        
        style_control_frame = tk.Frame(style_frame, bg="#1a1a1a")
        style_control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Style checkboxes
        self.bold_var = tk.BooleanVar(value=self.font_manager.current_font['weight'] == 'bold')
        self.italic_var = tk.BooleanVar(value=self.font_manager.current_font['slant'] == 'italic')
        self.underline_var = tk.BooleanVar(value=self.font_manager.current_font['underline'] == 1)
        self.strikethrough_var = tk.BooleanVar(value=self.font_manager.current_font['overstrike'] == 1)
        
        tk.Checkbutton(style_control_frame, text="Bold", variable=self.bold_var,
                      bg="#1a1a1a", fg="#ffffff", selectcolor="#2d2d2d",
                      font=("Cascadia Code", 10)).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Checkbutton(style_control_frame, text="Italic", variable=self.italic_var,
                      bg="#1a1a1a", fg="#ffffff", selectcolor="#2d2d2d",
                      font=("Cascadia Code", 10)).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Checkbutton(style_control_frame, text="Underline", variable=self.underline_var,
                      bg="#1a1a1a", fg="#ffffff", selectcolor="#2d2d2d",
                      font=("Cascadia Code", 10)).pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Checkbutton(style_control_frame, text="Strikethrough", variable=self.strikethrough_var,
                      bg="#1a1a1a", fg="#ffffff", selectcolor="#2d2d2d",
                      font=("Cascadia Code", 10)).pack(side=tk.LEFT)
        
        # Color Section
        color_frame = tk.LabelFrame(main_frame, text="Colors", bg="#1a1a1a", fg="#23c4a4",
                                  font=("Cascadia Code", 12, "bold"))
        color_frame.pack(fill=tk.X, pady=(0, 15))
        
        color_control_frame = tk.Frame(color_frame, bg="#1a1a1a")
        color_control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Color buttons
        tk.Button(color_control_frame, text="Text Color", command=self.change_text_color,
                 bg="#2d2d2d", fg="#ffffff", font=("Cascadia Code", 10),
                 width=12).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(color_control_frame, text="Background Color", command=self.change_background_color,
                 bg="#2d2d2d", fg="#ffffff", font=("Cascadia Code", 10),
                 width=15).pack(side=tk.LEFT, padx=(0, 10))
        
        # Color preview
        self.color_preview = tk.Label(color_control_frame, text="Preview", width=10, height=2,
                                    bg=self.font_manager.current_font['background'],
                                    fg=self.font_manager.current_font['foreground'],
                                    font=("Cascadia Code", 10))
        self.color_preview.pack(side=tk.LEFT, padx=(20, 0))
        
        # Preview Section
        preview_frame = tk.LabelFrame(main_frame, text="Preview", bg="#1a1a1a", fg="#23c4a4",
                                    font=("Cascadia Code", 12, "bold"))
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.preview_text = tk.Text(preview_frame, height=4, bg="#2d2d2d", fg="#ffffff",
                                  font=("Cascadia Code", 12), wrap=tk.WORD)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.preview_text.insert("1.0", "The quick brown fox jumps over the lazy dog.\n" +
                                        "1234567890 !@#$%^&*()\n" +
                                        "This is a preview of your selected font.")
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg="#1a1a1a")
        button_frame.pack(fill=tk.X)
        
        # Buttons
        tk.Button(button_frame, text="Apply", command=self.apply_changes,
                 bg="#23c4a4", fg="#1a1a1a", font=("Cascadia Code", 11, "bold"),
                 width=10).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="Preview", command=self.preview_changes,
                 bg="#2d2d2d", fg="#ffffff", font=("Cascadia Code", 11),
                 width=10).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="Reset", command=self.reset_to_default,
                 bg="#2d2d2d", fg="#ffffff", font=("Cascadia Code", 11),
                 width=10).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="Cancel", command=self.dialog.destroy,
                 bg="#2d2d2d", fg="#ffffff", font=("Cascadia Code", 11),
                 width=10).pack(side=tk.RIGHT)
        
        # Bind events
        self.family_listbox.bind('<<ListboxSelect>>', self.on_family_select)
        self.size_spinbox.bind('<KeyRelease>', self.on_size_change)
        
        # Initial preview update
        self.preview_changes()
    
    def set_quick_size(self, size):
        """Set font size using quick size buttons"""
        self.size_var.set(str(size))
        self.preview_changes()
    
    def on_family_select(self, event):
        """Handle font family selection"""
        self.preview_changes()
    
    def on_size_change(self, event):
        """Handle font size change"""
        self.preview_changes()
    
    def change_text_color(self):
        """Change text color"""
        color = colorchooser.askcolor(initialcolor=self.font_manager.current_font['foreground'])
        if color[1]:
            self.color_preview.config(fg=color[1])
            self.preview_text.config(fg=color[1])
    
    def change_background_color(self):
        """Change background color"""
        color = colorchooser.askcolor(initialcolor=self.font_manager.current_font['background'])
        if color[1]:
            self.color_preview.config(bg=color[1])
            self.preview_text.config(bg=color[1])
    
    def preview_changes(self):
        """Update the preview text with current settings"""
        try:
            # Get selected font family
            selection = self.family_listbox.curselection()
            if selection:
                family = self.family_listbox.get(selection[0])
            else:
                family = self.font_manager.current_font['family']
            
            # Get font size
            try:
                size = int(self.size_var.get())
            except ValueError:
                size = self.font_manager.current_font['size']
            
            # Get font style
            weight = 'bold' if self.bold_var.get() else 'normal'
            slant = 'italic' if self.italic_var.get() else 'roman'
            underline = 1 if self.underline_var.get() else 0
            overstrike = 1 if self.strikethrough_var.get() else 0
            
            # Create font object
            preview_font = font.Font(
                family=family,
                size=size,
                weight=weight,
                slant=slant,
                underline=underline,
                overstrike=overstrike
            )
            
            # Apply to preview
            self.preview_text.config(font=preview_font)
            
        except Exception as e:
            print(f"Error updating preview: {e}")
    
    def apply_changes(self):
        """Apply the selected font settings"""
        try:
            # Get selected font family
            selection = self.family_listbox.curselection()
            if selection:
                family = self.family_listbox.get(selection[0])
                self.font_manager.current_font['family'] = family
            
            # Get font size
            try:
                size = int(self.size_var.get())
                if 6 <= size <= 72:
                    self.font_manager.current_font['size'] = size
            except ValueError:
                pass
            
            # Get font style
            self.font_manager.current_font['weight'] = 'bold' if self.bold_var.get() else 'normal'
            self.font_manager.current_font['slant'] = 'italic' if self.italic_var.get() else 'roman'
            self.font_manager.current_font['underline'] = 1 if self.underline_var.get() else 0
            self.font_manager.current_font['overstrike'] = 1 if self.strikethrough_var.get() else 0
            
            # Get colors
            self.font_manager.current_font['foreground'] = self.color_preview.cget('fg')
            self.font_manager.current_font['background'] = self.color_preview.cget('bg')
            
            # Apply changes
            self.font_manager.apply_font()
            self.font_manager.save_font_config()
            
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply font changes: {e}")
    
    def reset_to_default(self):
        """Reset all settings to default"""
        # Reset variables
        self.size_var.set("12")
        self.bold_var.set(False)
        self.italic_var.set(False)
        self.underline_var.set(False)
        self.strikethrough_var.set(False)
        
        # Reset colors
        self.color_preview.config(fg="#d4d4d4", bg="#1e1e1e")
        self.preview_text.config(fg="#d4d4d4", bg="#1e1e1e")
        
        # Reset font family selection
        try:
            fonts = self.font_manager.get_available_fonts()
            default_family = preferred_mono_font_family(self.parent)
            default_index = fonts.index(default_family)
            self.family_listbox.selection_clear(0, tk.END)
            self.family_listbox.selection_set(default_index)
            self.family_listbox.see(default_index)
        except ValueError:
            pass
        
        self.preview_changes()


# Convenience functions for easy integration
def create_font_manager(text_widget):
    """Create and return a FontManager instance"""
    return FontManager(text_widget)

def show_font_dialog(text_widget, parent=None):
    """Show font dialog for the given text widget"""
    font_manager = FontManager(text_widget)
    font_manager.show_font_dialog(parent)
    return font_manager