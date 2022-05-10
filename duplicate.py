# MIT License
#
# Copyright (c) 2022 H. Thevindu J. Wijesekera
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


from os import path, walk, remove
from filecmp import cmp
import hashlib
from traceback import format_exc

def compare_list(file_list):
    if len(file_list) == 2:
        if cmp(file_list[0], file_list[1], False):
            yield file_list
        return
    hashes = {}
    for file_name in file_list:
        try:
            sha256 = hashlib.sha256()
            with open(file_name, 'rb') as file:
                while True:
                    buffer = file.read(4096)
                    if not buffer:
                        break
                    sha256.update(buffer)
                digest = sha256.digest()
                if digest not in hashes:
                    hashes[digest] = [file_name]
                else:
                    hashes[digest].append(file_name)
        except: pass
    for duplicates in hashes.values():
        if len(duplicates)>1:
            yield duplicates


def sample_check(size, file_list, sample_cnt):
    sample_map = {}
    sample_arr = bytearray(sample_cnt)
    step = size//sample_cnt
    for file_name in file_list:
        try:
            with open(file_name, 'rb') as file:
                for off in range(sample_cnt):
                    file.seek(off*step, 0)
                    buffer = file.read(1)
                    if not buffer:
                        break
                    sample_arr[off] = buffer[0]
                sample = bytes(sample_arr)
                if sample not in sample_map:
                    sample_map[sample] = [file_name]
                else:
                    sample_map[sample].append(file_name)
        except: pass
    for duplicates in sample_map.values():
        if len(duplicates)>1:
            yield duplicates


def compare_file_list(size, file_list):
    if size<=50:
        for duplicate in compare_list(file_list):
            yield duplicate
        return
    for l5 in sample_check(size, file_list, 5):
        if size<5000:
            for duplicate in compare_list(l5):
                yield duplicate
            continue
        for l31 in sample_check(size, l5, 31):
            if size<100000:
                for duplicate in compare_list(l31):
                    yield duplicate
                continue
            for l101 in sample_check(size, l31, 101):
                for duplicate in compare_list(l101):
                    yield duplicate


def duplicate_remove(root, MIN_SIZE=-1):
    # dictionary with file size as key and list file names as value
    size_dict = dict()
    try:
        for l in walk(root):
            files = l[2] # list of file names in the directory
            for file_name in files:
                p = path.join(l[0], file_name)
                if path.islink(p): continue
                size = path.getsize(p) # size of file
                if MIN_SIZE <= size:
                    if size in size_dict: # if that size is already available
                        size_dict[size].append(p)
                    else:
                        size_dict[size] = [p]
    except KeyboardInterrupt:
        pass

    #remove file names with no duplicates
    try:
        no_duplicates = [] # file sizes with no duplicate files
        for size in size_dict:
            if len(size_dict[size])==1:
                no_duplicates.append(size)
        for size in no_duplicates:
            size_dict.pop(size)

        sizes = sorted(size_dict.keys(), reverse=True) #sort by size. Largest first
        root_len = len(root) #length of root_dir name
        for size in sizes:
            l = size_dict.pop(size)

            # iterate through duplicate lists and
            # prompt user to select which files to remove
            for dup_list in compare_file_list(size, l):
                print("Size = %i bytes"%size)
                for i in range(len(dup_list)):
                    print("%i) %s" % (i+1, dup_list[i][root_len:])) # print 1 based indices
                print()
                try:
                    remove_list = tuple(map(int, input("Enter space separated list of indices to remove : ").strip().split()))
                    for index in remove_list:
                        index -= 1  # convert to 0 based index
                        if 0<=index<len(dup_list):
                            remove(dup_list[index])
                except ValueError:
                    pass
                print("\n")
    except KeyboardInterrupt:
        pass

root = input("Enter path : ")
duplicate_remove(root, 1)