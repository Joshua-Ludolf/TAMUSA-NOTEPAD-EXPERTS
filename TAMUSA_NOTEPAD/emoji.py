import tkinter as tk
from tkinter import ttk, Toplevel

class EmojiPicker:
    """A popup window for selecting emojis"""
    
    def __init__(self, parent, callback):
        self.callback = callback
        self.window = Toplevel(parent)
        self.window.title("Insert Emoji")
        self.window.geometry("600x400")
        self.window.configure(bg="#1e1e1e")
        self.window.resizable(True, True)
        
        # Make it modal
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center the window
        self.window.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title label
        title_label = tk.Label(
            self.window,
            text="Select an Emoji",
            font=("Cascadia Code", 14, "bold"),
            bg="#1e1e1e",
            fg="#23c4a4"
        )
        title_label.pack(pady=10)
        
        # Search frame
        search_frame = tk.Frame(self.window, bg="#1e1e1e")
        search_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(
            search_frame,
            text="Search:",
            font=("Cascadia Code", 10),
            bg="#1e1e1e",
            fg="#d4d4d4"
        ).pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Cascadia Code", 10),
            bg="#2d2d2d",
            fg="#d4d4d4",
            insertbackground="#23c4a4",
            relief=tk.FLAT,
            bd=5
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        self.search_var.trace('w', self.filter_emojis)
        
        # Emoji categories
        categories_frame = tk.Frame(self.window, bg="#1e1e1e")
        categories_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.category_var = tk.StringVar(value="All")
        categories = ["All", "Smileys", "People", "Nature", "Food", "Activities", "Travel", "Objects", "Symbols", "Flags"]
        
        for category in categories:
            btn = tk.Radiobutton(
                categories_frame,
                text=category,
                variable=self.category_var,
                value=category,
                command=self.filter_emojis,
                font=("Cascadia Code", 8),
                bg="#1e1e1e",
                fg="#d4d4d4",
                selectcolor="#2d2d2d",
                activebackground="#3e3e3e",
                activeforeground="#23c4a4"
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # Emoji grid frame with scrollbar
        self.canvas = tk.Canvas(self.window, bg="#1e1e1e", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#1e1e1e")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        self.scrollbar.pack(side="right", fill="y", pady=10)
        
        # Bind mousewheel to canvas
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Create emoji data
        self.emoji_data = self.get_emoji_data()
        self.create_emoji_grid()
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def get_emoji_data(self):
        """Returns a comprehensive list of emojis organized by category"""
        return {
            "Smileys": [
                "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇",
                "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘", "😗", "😙", "😚",
                "😋", "😛", "😝", "😜", "🤪", "🤨", "🧐", "🤓", "😎", "🤩",
                "🥳", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹️", "😣",
                "😖", "😫", "😩", "🥺", "😢", "😭", "😤", "😠", "😡", "🤬"
            ],
            "People": [
                "👋", "🤚", "🖐️", "✋", "🖖", "👌", "🤏", "✌️", "🤞", "🤟",
                "🤘", "🤙", "👈", "👉", "👆", "🖕", "👇", "☝️", "👍", "👎",
                "✊", "👊", "🤛", "🤜", "👏", "🙌", "👐", "🤲", "🤝", "🙏",
                "👶", "🧒", "👦", "👧", "🧑", "👱", "👨", "🧔", "👩", "🧓"
            ],
            "Nature": [
                "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯",
                "🦁", "🐮", "🐷", "🐽", "🐸", "🐵", "🙈", "🙉", "🙊", "🐒",
                "🐔", "🐧", "🐦", "🐤", "🐣", "🐥", "🦆", "🦅", "🦉", "🦇",
                "🌸", "🌺", "🌻", "🌹", "🥀", "🌷", "🌼", "🌲", "🌳", "🌴"
            ],
            "Food": [
                "🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🍈", "🍒",
                "🍑", "🥭", "🍍", "🥥", "🥝", "🍅", "🍆", "🥑", "🥦", "🥬",
                "🥒", "🌶️", "🌽", "🥕", "🧄", "🧅", "🥔", "🍠", "🥐", "🍞",
                "🥖", "🥨", "🧀", "🥚", "🍳", "🧈", "🥞", "🧇", "🥓", "🥩"
            ],
            "Activities": [
                "⚽", "🏀", "🏈", "⚾", "🥎", "🎾", "🏐", "🏉", "🥏", "🎱",
                "🪀", "🏓", "🏸", "🏒", "🏑", "🥍", "🏏", "⛳", "🪁", "🏹",
                "🎣", "🤿", "🥊", "🥋", "🎽", "🛹", "🛷", "⛸️", "🥌", "🎿",
                "⛷️", "🏂", "🪂", "🏋️", "🤼", "🤸", "⛹️", "🤺", "🏇", "🧘"
            ],
            "Travel": [
                "🚗", "🚕", "🚙", "🚌", "🚎", "🏎️", "🚓", "🚑", "🚒", "🚐",
                "🛻", "🚚", "🚛", "🚜", "🏍️", "🛵", "🚲", "🛴", "🛺", "🚨",
                "🚔", "🚍", "🚘", "🚖", "🚡", "🚠", "🚟", "🚃", "🚋", "🚞",
                "🚝", "🚄", "🚅", "🚈", "🚂", "🚆", "🚇", "🚊", "🚉", "✈️"
            ],
            "Objects": [
                "⌚", "📱", "📲", "💻", "⌨️", "🖥️", "🖨️", "🖱️", "🖲️", "🕹️",
                "🗜️", "💽", "💾", "💿", "📀", "📼", "📷", "📸", "📹", "🎥",
                "📽️", "🎞️", "📞", "☎️", "📟", "📠", "📺", "📻", "🎙️", "🎚️",
                "🎛️", "🧭", "⏱️", "⏲️", "⏰", "🕰️", "⌛", "⏳", "📡", "🔋"
            ],
            "Symbols": [
                "❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "💔",
                "❣️", "💕", "💞", "💓", "💗", "💖", "💘", "💝", "💟", "☮️",
                "✝️", "☪️", "🕉️", "☸️", "✡️", "🔯", "🕎", "☯️", "☦️", "🛐",
                "⭐", "🌟", "✨", "⚡", "☄️", "💥", "🔥", "🌈", "☀️", "🌤️"
            ],
            "Flags": [
                "🏁", "🚩", "🎌", "🏴", "🏳️", "🏳️‍🌈", "🏳️‍⚧️", "🏴‍☠️", "🇺🇸", "🇨🇦",
                "🇲🇽", "🇧🇷", "🇦🇷", "🇬🇧", "🇫🇷", "🇩🇪", "🇮🇹", "🇪🇸", "🇷🇺", "🇨🇳",
                "🇯🇵", "🇰🇷", "🇮🇳", "🇦🇺", "🇿🇦", "🇪🇬", "🇳🇬", "🇰🇪", "🇬🇭", "🇲🇦"
            ]
        }
    
    def create_emoji_grid(self):
        """Create the grid of emoji buttons"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Get filtered emojis
        emojis = self.get_filtered_emojis()
        
        # Create grid
        row = 0
        col = 0
        max_cols = 12
        
        for emoji in emojis:
            btn = tk.Button(
                self.scrollable_frame,
                text=emoji,
                font=("Segoe UI Emoji", 20),
                bg="#2d2d2d",
                fg="#ffffff",
                activebackground="#3e3e3e",
                relief=tk.FLAT,
                bd=0,
                width=3,
                height=1,
                command=lambda e=emoji: self.insert_emoji(e)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Update scroll region
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def get_filtered_emojis(self):
        """Get emojis based on current filter settings"""
        category = self.category_var.get()
        search_term = self.search_var.get().lower()
        
        emojis = []
        
        if category == "All":
            for cat_emojis in self.emoji_data.values():
                emojis.extend(cat_emojis)
        else:
            emojis = self.emoji_data.get(category, [])
        
        # If there's a search term, we could implement emoji name searching
        # For now, just return the category-filtered emojis
        return emojis
    
    def filter_emojis(self, *args):
        """Filter emojis based on category and search"""
        self.create_emoji_grid()
    
    def insert_emoji(self, emoji):
        """Insert the selected emoji and close the picker"""
        self.callback(emoji)
        self.window.destroy()
