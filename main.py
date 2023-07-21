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
    if ui_controller != None:
        ui_controller.end()
    ui_controller = UIcontroller(root, list_container, size_label, canvas, dup_width)
    ui_controller.start()


def del_btn_clk():
    global ui_controller
    if ui_controller == None:
        return
    ui_controller.del_files()


def back_btn_clk():
    global ui_controller
    if ui_controller == None:
        return
    ui_controller.show_prev()


def next_btn_clk():
    global ui_controller
    if ui_controller == None:
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

home.rowconfigure(0, minsize=30, weight=1)
home.rowconfigure(1, weight=25)
home.rowconfigure(2, minsize=30, weight=1)
home.grid_columnconfigure(0, weight=1)
home.grid_propagate(False)

# Top frame
top_frame = tk.Frame(home, bg="gray", height=25, pady=5)
top_frame.grid(column=0, row=0, sticky=tk.NSEW)
top_frame.grid_propagate(False)

mid_frame = tk.Frame(home, bg="gray", height=25, padx=10, pady=5)
mid_frame.grid(column=0, row=1, sticky=tk.NSEW)
mid_frame.grid_propagate(False)

bottom_frame = tk.Frame(home, bg="gray", height=25, pady=2)
bottom_frame.grid(column=0, row=2, sticky=tk.NSEW)
bottom_frame.grid_propagate(False)

# Top frame
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

# Mid frame
mid_frame.columnconfigure(0, weight=1)
mid_frame.grid_rowconfigure(0, weight=1)

dup_container = tk.Frame(mid_frame, bg="white")
dup_container.grid(column=0, row=0, sticky=tk.NSEW)
dup_container.grid_propagate(False)

dup_container.rowconfigure(0, minsize=30, weight=1)
dup_container.rowconfigure(1, weight=100)
dup_container.grid_columnconfigure(0, weight=1)

size_label = tk.Label(dup_container, bg="white",
                      anchor="w", font="arial 14 bold")
size_label.grid(column=0, row=0, sticky=tk.NSEW, padx=30, pady=2)
size_label.grid_propagate(False)

list_frame = tk.Frame(dup_container, bg="white")
list_frame.grid(column=0, row=1, sticky=tk.NSEW)

def on_configure(exent):
    canvas.configure(scrollregion=canvas.bbox('all'))

def safe_yview(a,y):
    if float(y)<=0.:
        y = 0.
    canvas.yview(a,y)

canvas = tk.Canvas(list_frame, bd=0, highlightthickness=0)
canvas.pack(side=tk.LEFT, fill="both", expand=True)
scrollbar = tk.Scrollbar(list_frame, command=safe_yview)
scrollbar.pack(side=tk.LEFT, fill='y', expand=False)
canvas.configure(yscrollcommand = scrollbar.set)
canvas.bind('<Configure>', on_configure)
mid_frame.update()
scrollbar.update()
dup_width = mid_frame.winfo_width() - scrollbar.winfo_width() - 1
list_container = tk.Frame(canvas, width=dup_width)
canvas.create_window((0,0), window=list_container, anchor='nw')

# Bottom frame
bottom_frame.columnconfigure(0, weight=2)
bottom_frame.columnconfigure(1, weight=3)
bottom_frame.columnconfigure(2, weight=2)

bottom_frame.grid_rowconfigure(0, weight=1)

back_btn = tk.Button(bottom_frame, text="<Back", command=back_btn_clk)
back_btn.grid(column=0, row=0, sticky=tk.EW, padx=40, pady=2)
back_btn.grid_propagate(False)

del_btn = tk.Button(bottom_frame, text="Delete selected files",
                    bg="red", font="arial 14 bold", command=del_btn_clk)
del_btn.grid(column=1, row=0, sticky=tk.NSEW, padx=20, pady=2)

next_btn = tk.Button(bottom_frame, text="Next>", command=next_btn_clk)
next_btn.grid(column=2, row=0, sticky=tk.EW, padx=40, pady=2)
next_btn.grid_propagate(False)

list_container.update()

home.mainloop()
