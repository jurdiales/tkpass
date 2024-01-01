import os
import random
import time

import tkinter as tk
from tkinter import ttk     # themed tk widgets
import pyperclip
from tkinter.font import Font

from . import functions as f

PASS_MIN_LENGTH = 4
PASS_MAX_LENGTH = 32
PASS_DEFAULT_LENGTH = 8
PASS_LENGTH: int = 0
THEME = 'light'


class MainGUI:
    def __init__(self, frame: tk.Frame):
        self.frame = frame

        # password length
        self.top_frame = ttk.Frame(self.frame)
        self.length_lbl = ttk.Label(self.top_frame, text="Length:")
        self.length_txt = ttk.Spinbox(self.top_frame, width=20, 
                                      from_=PASS_MIN_LENGTH, to=PASS_MAX_LENGTH, increment=1)
        self.length_txt.insert(0, str(PASS_DEFAULT_LENGTH))

        # checks
        self.lower_state = tk.BooleanVar(self.frame)
        self.number_state = tk.BooleanVar(self.frame)
        self.upper_state = tk.BooleanVar(self.frame)
        self.symbol_state = tk.BooleanVar(self.frame)

        self.check_frame = ttk.Frame(self.frame)
        self.lower_chk = ttk.Checkbutton(self.check_frame, text='Lower Case', variable=self.lower_state)
        self.number_chk = ttk.Checkbutton(self.check_frame, text='Numbers', variable=self.number_state)
        self.upper_chk = ttk.Checkbutton(self.check_frame, text='Upper Case', variable=self.upper_state)
        self.symbol_chk = ttk.Checkbutton(self.check_frame, text='Symbols', variable=self.symbol_state)

        # password generator part
        self.pass_lbl = ttk.Label(self.frame, text="Generated password:", font='bold')
        font = Font(self.frame, font=self.pass_lbl['font'])
        self.pass_lbl.configure(font=(font.cget('family'), 12, 'bold'))
        self.pass_txt = ttk.Entry(self.frame, width=38, justify='center', font='TkFixedFont')
        
        self.entropy_frame = ttk.Frame(self.frame)
        self.entropy_bar_w_val = tk.IntVar(self.frame)
        self.entropy_bar_m_val = tk.IntVar(self.frame)
        self.entropy_bar_s_val = tk.IntVar(self.frame)
        self.entropy_bar_w = ttk.Progressbar(self.entropy_frame, orient=tk.HORIZONTAL, variable=self.entropy_bar_w_val)    # range from 0 to 100
        self.entropy_bar_m = ttk.Progressbar(self.entropy_frame, orient=tk.HORIZONTAL, variable=self.entropy_bar_m_val)    # range from 0 to 100
        self.entropy_bar_s = ttk.Progressbar(self.entropy_frame, orient=tk.HORIZONTAL, variable=self.entropy_bar_s_val)    # range from 0 to 100
        self.weak_lbl = ttk.Label(self.entropy_frame, text="weak", foreground='black')        # #a83232
        self.medium_lbl = ttk.Label(self.entropy_frame, text="medium", foreground='black')    # #a6a832
        self.strong_lbl = ttk.Label(self.entropy_frame, text="strong", foreground='black')    # #32a83e

        self.bottom_frame = ttk.Frame(self.frame)
        self.pass_btn = ttk.Button(self.bottom_frame, text="Generate", command=self.on_generate_pressed, width=10)
        self.pass_cpy = ttk.Button(self.bottom_frame, text="Copy", command=self.on_copy_pressed, width=10)

        self.configure()
    
    def configure(self):
        self.top_frame.pack(pady=10, expand=True)
        self.length_lbl.pack(side=tk.LEFT, padx=(0, 5))
        self.length_txt.pack(side=tk.RIGHT)

        self.check_frame.pack(expand=True)
        self.lower_state.set(True)
        self.lower_chk.grid(row=0, column=0, padx=(0, 5), pady=(0, 5), sticky="W")  # left justify
        self.upper_chk.grid(row=1, column=0, padx=(0, 5), pady=(5, 0), sticky="W")  # left justify
        self.number_chk.grid(row=0, column=1, padx=(5, 0), pady=(0, 5), sticky="W") # left justify
        self.symbol_chk.grid(row=1, column=1, padx=(5, 0), pady=(5, 0), sticky="W") # left justify

        self.pass_lbl.pack(pady=(15,10))
        self.pass_txt.pack()

        self.entropy_frame.pack(pady=(10, 0), expand=True)
        self.entropy_bar_w.grid(row=0, column=0, sticky="W")
        self.entropy_bar_m.grid(row=0, column=1, padx=10)
        self.entropy_bar_s.grid(row=0, column=2, sticky="E")
        self.weak_lbl.grid(row=1, column=0)
        self.medium_lbl.grid(row=1, column=1)
        self.strong_lbl.grid(row=1, column=2)
        self.bottom_frame.pack(pady=10)
        self.pass_btn.grid(row=0, column=0, padx=(0, 20))
        self.pass_cpy.grid(row=0, column=1, padx=(20, 0))

    def on_generate_pressed(self):
        try:
            PASS_LENGTH = int(self.length_txt.get())
        except:
            PASS_LENGTH = 8
        PASS_LENGTH = f.clamp(PASS_LENGTH, PASS_MIN_LENGTH, PASS_MAX_LENGTH)
        self.pass_txt.delete(0, tk.END)
        password, entropy = f.generate_password(PASS_LENGTH, self.lower_state.get(), self.number_state.get(), 
                                                self.upper_state.get(), self.symbol_state.get())
        self.pass_txt.insert(0, password)
        entropy = f.clamp(entropy - 10, 0, 100) # minimum entropy is 14
        if entropy < 33:
            # 0 to 33 -> 0 to 100
            val = int((f.clamp(entropy, 0, 33) / 33) * 100)
            self.entropy_bar_w_val.set(val)
            self.entropy_bar_m_val.set(0)
            self.entropy_bar_s_val.set(0)
        elif entropy < 66:
            # 33 to 66 -> 0 to 100
            val = int((f.clamp(entropy, 33, 66) - 33) / 33 * 100)
            self.entropy_bar_w_val.set(100)
            self.entropy_bar_m_val.set(val)
            self.entropy_bar_s_val.set(0)
        else:
            # 66 to 100 -> 0 to 100
            val = int((f.clamp(entropy, 66, 100) - 66) / 34 * 100)
            self.entropy_bar_w_val.set(100)
            self.entropy_bar_m_val.set(100)
            self.entropy_bar_s_val.set(val)

    def on_copy_pressed(self):
        pyperclip.copy(self.pass_txt.get())


def run(theme: str = THEME):
    random.seed(int(time.time()) + PASS_LENGTH + random.randint(0, 255))
    dir_path = os.path.dirname(os.path.realpath(__file__))
    THEME = theme

    # root window
    root = tk.Tk()
    root.title("Password Generator")
    root.iconbitmap(os.path.join(dir_path, 'password.ico'))
    root.option_add("*tearOff", False) # This is always a good idea

    if theme == 'light':
        # Import the tcl file
        root.tk.call("source", os.path.join(dir_path, 'azure.tcl'))
        # set theme
        root.tk.call("set_theme", "light")
    elif theme == 'dark':
        # Import the tcl file
        root.tk.call("source", os.path.join(dir_path, 'azure.tcl'))
        # set theme
        root.tk.call("set_theme", "dark")
    elif theme == 'forestdark':
        # Import the tcl file
        root.tk.call('source', os.path.join(dir_path, 'forest-dark.tcl'))
        # Set the theme with the theme_use method
        ttk.Style().theme_use('forest-dark')
    elif theme == 'forestlight':
        # Import the tcl file
        root.tk.call('source', os.path.join(dir_path, 'forest-light.tcl'))
        # Set the theme with the theme_use method
        ttk.Style().theme_use('forest-light')

    # main frame inside root window
    frame = ttk.Frame(root)
    frame.grid(padx=10, sticky="nsew")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    _ = MainGUI(frame)
    root.mainloop()

if __name__ == '__main__':
    run()
