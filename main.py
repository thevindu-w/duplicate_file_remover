# MIT License
#
# Copyright (c) 2022 thevindu-w
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import tkinter as tk
from tkinter import filedialog
from controller import UIcontroller

ui_controller = None

def browse_btn_clk():
    folder_selected = filedialog.askdirectory()
    input_path.delete(0, 'end')
    input_path.insert(0, folder_selected)


def scan_btn_clk():
    global ui_controller
    root = input_path.get()
    if ui_controller!=None:
        ui_controller.end()
    ui_controller = UIcontroller(root, list_container, size_label)
    ui_controller.start()

def del_btn_clk():
    # TODO: Implement
    pass


def back_btn_clk():
    global ui_controller
    if ui_controller==None:
        return
    ui_controller.show_prev()


def next_btn_clk():
    global ui_controller
    if ui_controller==None:
        return
    ui_controller.show_next()


home = tk.Tk()

home.title("Duplicate Remove")

screen_width = home.winfo_screenwidth()
screen_height = home.winfo_screenheight()

win_width = int(screen_width*0.6)
win_height = int(screen_height*0.6)

home.geometry("%ix%i+%i+%i" % (int(screen_width*0.6),
              int(screen_height*0.6), int(screen_width*0.2), int(screen_height*0.2)))
home.resizable(False, False)

home.rowconfigure(0, minsize=25, weight=1)
home.rowconfigure(1, weight=25)
home.grid_columnconfigure(0, weight=1)
home.grid_propagate(False)

# Top frame
top_frame = tk.Frame(home, bg="gray", height=25, pady=5)
top_frame.grid(column=0, row=0, sticky=tk.NSEW)
top_frame.grid_propagate(False)

top_frame.columnconfigure(0, weight=2)
top_frame.columnconfigure(1, weight=30)
top_frame.columnconfigure(2, weight=2)
top_frame.columnconfigure(3, weight=3)

enter_label = tk.Label(top_frame, text="Enter Path :", bg="gray")
enter_label.grid(column=0, row=0, sticky=tk.E, padx=2, pady=2)

input_path = tk.Entry(top_frame, bg="white")
input_path.grid(column=1, row=0, sticky=tk.EW, padx=2, pady=2)

browse_btn = tk.Button(top_frame, text="Browse", command=browse_btn_clk)
browse_btn.grid(column=2, row=0, sticky=tk.EW, padx=5, pady=2)

scan_btn = tk.Button(top_frame, text="Scan", bg="green",
                     font="arial 13 bold", command=scan_btn_clk)
scan_btn.grid(column=3, row=0, sticky=tk.EW, padx=5, pady=2)


bottom_frame = tk.Frame(home, bg="gray")
bottom_frame.grid(column=0, row=1, sticky=tk.NSEW)
bottom_frame.grid_propagate(False)

bottom_frame.columnconfigure(0, weight=1)
bottom_frame.columnconfigure(1, weight=30)
bottom_frame.columnconfigure(2, weight=1)

bottom_frame.grid_rowconfigure(0, weight=1)


back_btn = tk.Button(bottom_frame, text="<Back", command=back_btn_clk)
back_btn.grid(column=0, row=0, sticky=tk.EW, padx=2, pady=2)

next_btn = tk.Button(bottom_frame, text="Next>", command=next_btn_clk)
next_btn.grid(column=2, row=0, sticky=tk.EW, padx=2, pady=2)


mid_frame = tk.Frame(bottom_frame, bg="gray", pady=5)
mid_frame.grid(column=1, row=0, sticky=tk.NSEW)
# mid_frame.grid_propagate(False)

mid_frame.rowconfigure(0, weight=25)
mid_frame.rowconfigure(1, minsize=30, weight=1)
mid_frame.grid_columnconfigure(0, weight=1)
# mid_frame.grid_propagate(False)

dup_container = tk.Frame(mid_frame, bg="white")
dup_container.grid(column=0, row=0, sticky=tk.NSEW)

dup_container.rowconfigure(0, minsize=30, weight=1)
dup_container.rowconfigure(1, weight=50)
dup_container.grid_columnconfigure(0, weight=1)

size_label = tk.Label(dup_container, bg="white",
                      anchor="w", font="arial 14 bold")
size_label.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=2)

list_container = tk.Frame(dup_container, bg="white", pady=2)
list_container.grid(column=0, row=1, sticky=tk.NSEW)

btn_container = tk.Frame(mid_frame, bg="gray", pady=5)
btn_container.grid(column=0, row=1, sticky=tk.NSEW)
# btn_container.grid_propagate(False)

btn_container.columnconfigure(0, weight=1)
btn_container.columnconfigure(1, minsize=60)
btn_container.columnconfigure(2, weight=1)
btn_container.grid_propagate(False)

tk.Frame(btn_container, bg="gray").grid(column=0, row=0, sticky=tk.NSEW)
tk.Frame(btn_container, bg="gray").grid(column=2, row=0, sticky=tk.NSEW)

del_btn = tk.Button(btn_container, text="Delete selected files",
                    bg="red", font="arial 14 bold", command=del_btn_clk)
del_btn.grid(column=1, row=0, sticky=tk.NSEW, padx=2, pady=2)

list_container.update()

home.mainloop()
