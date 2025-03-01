import tkinter as tk
import tkinter.dialog
import tkinter.filedialog
import tkinter.simpledialog
import os
import io
import sys

from mhscr_interpreter.main import IDE_Run
root = tk.Tk()
root.title("mhscr IDE")

frame = tk.Frame(root, bg='light blue')
frame.pack(fill='both', expand=True)

text_area = tk.Text(frame, width=80, height=20)
text_area.pack(fill='both', expand=True)

def saveFile():
    filename = tkinter.filedialog.asksaveasfilename(title="Save file")
    if filename:
        with open(filename, 'w') as f:
            script_content = text_area.get(1.0, tk.END)
            if script_content:
                f.write(script_content)

def openFile():
    filename = tkinter.filedialog.askopenfilename(title="Open file", filetypes=[("Text documents", "*.txt")])
    if filename:
        with open(filename, 'r') as file:
            content = file.read()
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.INSERT, content)

def runScript():
    script_content = text_area.get(1.0, tk.END)
    if script_content:
        with open('temp.txt', 'w') as f:
            f.write(script_content)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        IDE_Run()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        tk.messagebox.showinfo("Result", f"Script result:\n{output}")
        os.remove('temp.txt')
    else:
        tk.messagebox.showerror("Error", "No script to run.")

def cut():
    text_area.select_range(0, tk.END)
    text_area.delete(1.0, tk.END)

def copy():
    text_area.select_range(0, tk.END)
    text_area.event_generate("<<Copy>>")

def paste():
    clipboard_text = tkinter.simpledialog.askstring("Paste", "Enter pasted text:")
    if clipboard_text:
        text_area.insert(tk.CURSEL, clipboard_text)
# Run Button
run_button = tk.Button(frame, text="Run", command=runScript)
run_button.pack(side='bottom')

# Menu Bar
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Save", command=saveFile)
file_menu.add_command(label="Open...", command=openFile)

edit_menu = tk.Menu(menu)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)

root.mainloop()