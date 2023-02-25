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


import ctypes
from os import remove
import threading
from threading import Lock, Thread
import tkinter as tk
from tkinter.messagebox import askyesno
from duplicate import get_duplicates


class UIcontroller(Thread):
    def __init__(self, root, list_container, size_label, canvas, dup_width):
        Thread.__init__(self)
        self.listLock = Lock()
        self.duplicates = []
        self.check_list = []
        self.index = None
        self.root = root
        self.size_label = size_label
        self.list_container = list_container
        self.canvas = canvas
        self.dup_width = dup_width

    def run(self):
        try:
            for dup_list in get_duplicates(self.root):
                self.listLock.acquire()
                self.duplicates.append(dup_list)
                if self.index == None:
                    self.index = -1
                    self.listLock.release()
                    self.show_next()
                else:
                    self.listLock.release()
        except:
            pass

    def show_next(self):
        try:
            self.listLock.acquire()
            if self.index == None:
                self.listLock.release()
                return
            ind = self.index + 1
            if ind >= len(self.duplicates):
                self.listLock.release()
                return
            size, dup_list = self.duplicates[ind]
            self.index = ind
            self.__update_view(size, dup_list)
            self.listLock.release()
        except:
            pass

    def show_prev(self):
        try:
            self.listLock.acquire()
            if self.index == None or self.index <= 0:
                self.listLock.release()
                return
            ind = self.index - 1
            size, dup_list = self.duplicates[ind]
            self.index = ind
            self.__update_view(size, dup_list)
            self.listLock.release()
        except:
            pass

    def del_files(self):
        try:
            self.listLock.acquire()
            del_list = [elem for elem in self.check_list if elem[0].get()]
            self.listLock.release()
            if not del_list:
                return
            del_name_list = [elem[1] for elem in del_list]
            message = "Are you sure you want to delete the following files?\n" + \
                '\n'.join(fname[len(self.root):] for fname in del_name_list)
            choice = askyesno("Confirm delete", message)
            if choice:
                self.listLock.acquire()
                for elem in del_list:
                    fname = elem[1]
                    self.check_list.remove(elem)
                    elem[3].remove(fname)
                    elem[2].destroy()
                    remove(fname)
                self.listLock.release()
                self.list_container.update()
                self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        except:
            pass

    def __update_view(self, size, dup_list):
        self.size_label.config(text="Size : %i bytes" % size)
        for old_container in self.list_container.winfo_children():
            old_container.destroy()
        self.check_list = []
        odd = False
        for dup_name in dup_list:
            col = 0xbb if odd else 0xcc
            self.__append_dup_file(dup_name, dup_list, "#%02x%02x%02x"%(col,col,col))
            odd = not odd
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def __append_dup_file(self, file_name, parent_list, color):
        file_container = tk.Frame(
            self.list_container, bg=color, pady=1, padx=1)
        file_container.columnconfigure(0, weight=1, minsize=30)
        file_container.columnconfigure(1, weight=1000)
        boolVar = tk.BooleanVar()
        chk_box = tk.Checkbutton(
            file_container, bg=color, variable=boolVar, highlightthickness=0, bd=0)
        chk_box.grid(column=0, row=0, sticky=tk.NSEW, padx=0, pady=0)
        chk_box.update()
        width = self.dup_width - chk_box.winfo_width()
        fname_label = tk.Label(file_container, bg=color, width=width, text=file_name[len(self.root):],
                               anchor="w", font="arial 12", wraplength=width-2, justify="left")
        fname_label.grid(column=1, row=0, sticky=tk.NSEW, padx=2, pady=1)
        file_container.pack(fill="x")
        self.check_list.append(
            (boolVar, file_name, file_container, parent_list))

    def __get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def end(self):
        thread_id = self.__get_id()
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            thread_id, ctypes.py_object(SystemExit))
        self.listLock.acquire()
        self.duplicates.clear()
        self.duplicates = None
        self.list_container = None
        self.size_label = None
        self.listLock.release()
