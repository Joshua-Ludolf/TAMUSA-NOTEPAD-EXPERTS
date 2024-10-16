"""
    Group: TAMUSA Notepad Experts (TNE)
    Authors: Joshua Ludolf & Luis Morales
    Class: CSCI 3366 - Programming Languages

"""

import tkinter as tk
from tkinter import scrolledtext, Menu, filedialog

class NotePad:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1920x1080")
        self.root.title("TAMUSA Notepad")
        self.create_widgets()

    def create_widgets(self):
        self.create_menu_bar()
        self.message_box = scrolledtext.ScrolledText(self.root, font="TimesNewRoman", width=210, height=210)
        self.message_box.configure(bg="#2e2e2e")
        self.message_box.grid(row=1, column=0, columnspan=3, rowspan=3)

    def create_menu_bar(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)
        
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.configure(bg="#2e2e2e", foreground="#23c4a4")
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Open", command=self.open_file)

    def new_file(self):
        self.entry_text.delete("0", "end")
        self.message_box.delete("1.0", "end")

    def save_file(self):
        message = self.message_box.get("1.0", "end")
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text files", "*.txt"),
                                                                ("All files", "*.*")])
            if file_path:
                with open(file_path, "w") as file_name:
                    file_name.write(message)
        except Exception as e:
            self.message_box.insert(tk.INSERT, f"Error: {e}")

    def open_file(self):
        msg = ""
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"),
                                                              ("All files", "*.*")])
            if file_path:
                with open(file_path, "r") as in_file:
                    msg = in_file.read()
                    self.message_box.delete("1.0", "end")
                    self.message_box.insert(tk.INSERT, msg)
        except FileNotFoundError:
            self.message_box.insert(tk.INSERT, "File was not found! Please provide an existing file.")

def main():
    root = tk.Tk()
    root.configure(bg="#2e2e2e")
    app = NotePad(root)
    root.mainloop()

if __name__ == "__main__":
    main()
