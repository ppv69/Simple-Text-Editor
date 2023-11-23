import tkinter as tk
from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import re

from PIL import Image, ImageTk
import os

# Creating all the functions of all the buttons in the NotePad
def open_file(event=None):
    global file
    file = fd.askopenfilename(defaultextension='.txt', filetypes=[('All Files', '*.*'), ("Text File", "*.txt*")])

    if file != '':
        root.title(f"{os.path.basename(file)}")
        text_area.delete(1.0, END)
        with open(file, "r") as file_:
            text_area.insert(1.0, file_.read())
            file_.close()
    else:
        file = None


def open_new_file():
    root.title("Untitled - Notepad")
    text_area.delete(1.0, END)

def save_file(event=None):  # Add 'event=None' to accept an optional event argument
    global file
    
    if file:
        # Get the content from the text area
        content = text_area.get(1.0, END)
        
        # Open the file in write mode and write the content
        with open(file, "w") as file_:
            file_.write(content)
        
        # Update the Notepad window title with the filename
        root.title(f"{os.path.basename(file)} - Notepad")
    else:
        # If 'file' is empty, prompt the user to choose a file location and save as a new file
        save_as()

def save_as(event=None):  # Add 'event=None' to accept an optional event argument
    global file
    
    # Get the content from the text area
    content = text_area.get(1.0, END)
    
    # Always prompt the user to choose a file location
    file = fd.asksaveasfilename(
        initialfile='Untitled.txt',
        defaultextension='.txt',
        filetypes=[("Text File", "*.txt*"), ("Word Document", '*.docx*'), ("PDF", "*.pdf*")]
    )
    
    # Check if the user canceled the save operation (file is still None)
    if file:
        # Open the file in write mode and write the content
        with open(file, "w") as file_:
            file_.write(content)
        
        # Update the Notepad window title with the filename
        root.title(f"{os.path.basename(file)} - Notepad")
        
def find_text(event=None):
    find_window = tk.Toplevel(root)
    find_window.title("Find")
    find_window.geometry('300x100')

    find_label = tk.Label(find_window, text="Find:")
    find_label.pack()

    find_entry = tk.Entry(find_window)
    find_entry.pack()

    # Configure a "found" tag for highlighting
    text_area.tag_configure("found", background="yellow")

    def find_next():
        text_to_find = find_entry.get()
        if text_to_find:
            start_pos = "1.0"
            while True:
                start_pos = text_area.search(text_to_find, start_pos, nocase=True, stopindex=END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(text_to_find)}c"
                text_area.tag_add("found", start_pos, end_pos)
                text_area.see(start_pos)
                start_pos = end_pos

    find_button = tk.Button(find_window, text="Find", command=find_next)
    find_button.pack()

    find_window.bind("<Return>", lambda event: find_next())  # Bind Enter key to Find Next



def replace_text(event=None):
    replace_window = tk.Toplevel(root)
    replace_window.title("Replace")
    replace_window.geometry('300x150')

    find_label = tk.Label(replace_window, text="Find:")
    find_label.pack()

    find_entry = tk.Entry(replace_window)
    find_entry.pack()

    replace_label = tk.Label(replace_window, text="Replace with:")
    replace_label.pack()

    replace_entry = tk.Entry(replace_window)
    replace_entry.pack()

    def replace_this():
        text_to_find = find_entry.get()
        text_to_replace = replace_entry.get()
        if text_to_find and text_to_replace:
            text_area_text = text_area.get(1.0, END)
            updated_text = text_area_text.replace(text_to_find, text_to_replace, 1)
            text_area.delete(1.0, END)
            text_area.insert(1.0, updated_text)

    def replace_all():
        text_to_find = find_entry.get()
        text_to_replace = replace_entry.get()
        if text_to_find and text_to_replace:
            text_area_text = text_area.get(1.0, END)
            updated_text = text_area_text.replace(text_to_find, text_to_replace)
            text_area.delete(1.0, END)
            text_area.insert(1.0, updated_text)

    replace_this_button = tk.Button(replace_window, text="Replace This", command=replace_this)
    replace_this_button.pack()

    replace_all_button = tk.Button(replace_window, text="Replace All", command=replace_all)
    replace_all_button.pack()

def exit_application():
    root.destroy()


def copy_text():
    text_area.event_generate("<<Copy>>")


def cut_text():
    text_area.event_generate("<<Cut>>")


def paste_text():
    text_area.event_generate("<<Paste>>")


def select_all():
    text_area.event_generate("<<Control-Keypress-A>>")


def delete_last_char():
    text_area.event_generate("<<KP_Delete>>")
    

# Initializing the window
root = Tk()
root.title("Untitled - Notepad")
root.geometry('800x500')
root.resizable(0, 0)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

icon = ImageTk.PhotoImage(Image.open('Notepad.png'))
root.iconphoto(False, icon)
file = ''

# Setting the basic components of the window
menu_bar = Menu(root)
root.config(menu=menu_bar)

text_area = Text(root, font=("Times New Roman", 12))
text_area.grid(sticky=NSEW)

scroller = Scrollbar(text_area, orient=VERTICAL)
scroller.pack(side=RIGHT, fill=Y)

scroller.config(command=text_area.yview)
text_area.config(yscrollcommand=scroller.set)

# Adding the File Menu and its components
file_menu = Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')

file_menu.add_command(label="New", command=open_new_file)
file_menu.add_command(label="Open File", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Close File", command=exit_application)


menu_bar.add_cascade(label="File", menu=file_menu)

# Adding the Edit Menu and its components
edit_menu = Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')

edit_menu.add_command(label='Copy', command=copy_text)
edit_menu.add_command(label='Cut', command=cut_text)
edit_menu.add_command(label='Paste', command=paste_text)
edit_menu.add_command(label="Find", command=find_text)
edit_menu.add_command(label="Replace", command=replace_text)
edit_menu.add_separator()
edit_menu.add_command(label='Select All', command=select_all)
edit_menu.add_command(label='Delete', command=delete_last_char)

menu_bar.add_cascade(label="Edit", menu=edit_menu)

commands_menu =Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')
commands_menu.add_separator()
commands_menu.add_command(label="Open File = Ctrl+O", command=open_file)
commands_menu.add_command(label="Save = Ctrl+S", command=save_file)
commands_menu.add_command(label="Save As = Ctrl+Q", command=save_as)
commands_menu.add_separator()
commands_menu.add_command(label='Copy = Ctrl+C', command=copy_text)
commands_menu.add_command(label='Cut = Ctrl+X', command=cut_text)
commands_menu.add_command(label='Paste = Ctrl+V', command=paste_text)
commands_menu.add_command(label="Find = Ctrl+F", command=find_text)
commands_menu.add_command(label='Replace = Ctrl+H',command=replace_text)
commands_menu.add_separator()
commands_menu.add_command(label='Select All = Ctrl+A', command=select_all)
commands_menu.add_command(label='Delete = Delete Key', command=delete_last_char)

menu_bar.add_cascade(label="Shortcuts", menu=commands_menu)

root.bind("<Control-s>", save_file)
root.bind("<Control-q>", save_as)

# Adding the Find and Replace shortcuts
root.bind("<Control-f>", find_text)
root.bind("<Control-h>", replace_text)
root.bind("<Control-o>", open_file)

# Create a "found" tag for highlighting
text_area.tag_configure("found", background="yellow")


# Adding a label to the bottom that counts the number of characters in the text
# Label(root, text=f"{len(text_area.get(1.0, END))} characters", font=("Times New Roman", 12)).place(anchor=S, y=490)

# Finalizing the window
root.update()
root.mainloop()
