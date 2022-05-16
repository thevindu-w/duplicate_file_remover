import ctypes
import threading
from threading import Lock, Thread
from time import sleep
import tkinter as tk
from duplicate import get_duplicates


class UIcontroller(Thread):
    def __init__(self, root, list_container, size_label):
        Thread.__init__(self)
        self.listLock = Lock()
        self.duplicates = []
        self.index = None
        self.root = root
        self.size_label = size_label
        self.list_container = list_container

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
    
    def __update_view(self, size, dup_list):
        self.size_label.config(text="Size : %i bytes" % size)
        for old_container in self.list_container.winfo_children():
            old_container.destroy()
        for dup_name in dup_list:
            self.append_dup_file(dup_name)

    def append_dup_file(self, file_name):
        file_container = tk.Frame(
            self.list_container, bg="#aaaaaa", pady=1, padx=1)
        file_container.columnconfigure(0, weight=1, minsize=30)
        file_container.columnconfigure(1, weight=1000)
        chk_box = tk.Checkbutton(
            file_container, bg="#aaaaaa", highlightthickness=0, bd=0)
        chk_box.grid(column=0, row=0, sticky=tk.NSEW, padx=0, pady=0)
        chk_box.update()
        width = self.list_container.winfo_width() - chk_box.winfo_width() - 10
        fname_label = tk.Label(file_container, bg="#aaaaaa", text=file_name,
                               anchor="w", font="arial 12", wraplength=width, justify="left")
        fname_label.grid(column=1, row=0, sticky=tk.NSEW, padx=2, pady=1)
        file_container.pack(fill="x")
    
    def __get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def end(self):
        thread_id = self.__get_id()
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        self.listLock.acquire()
        self.duplicates.clear()
        self.duplicates = None
        self.list_container = None
        self.size_label = None
        self.listLock.release()
