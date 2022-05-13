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


from os import path, walk, remove
from filecmp import cmp
import hashlib


def compare_files(file_list):
    '''Compare a list of files and search for duplicates.

    Duplicates generated by this function are actual duplicates.
    If the file_list has more than 2 names, this uses SHA256 hash of the files to detect duplicates.
    Therefore it is assumed that SHA256 is collision resistant.

    :param file_list: List of file names
    :returns: Generator for duplicate files
    '''
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
        except:
            pass
    for duplicates in hashes.values():
        if len(duplicates) > 1:
            yield duplicates


def sample_util(size, file_list, sample_cnt):
    '''Compare a list of files having same size and search for possible duplicates.

    Duplicates generated by this function may NOT be duplicates.
    This may produce false positive results. But this will not produce false negative results.
    i.e. if this separates files as non-duplicate, they are actually non-duplicates.

    :param size: Size of each file in file_list (all files should have same size)
    :param file_list: List of file names
    :param sample_cnt: Number of samples to check
    :returns: Generator for possibly duplicate files
    '''
    sample_map = {}
    sample_arr = bytearray(sample_cnt)
    step = size//sample_cnt
    for file_name in file_list:
        try:
            with open(file_name, 'rb') as file:
                for off in range(sample_cnt):
                    file.seek((off+1)*step-1, 0)
                    buffer = file.read(1)
                    if not buffer:
                        break
                    sample_arr[off] = buffer[0]
                sample = bytes(sample_arr)
                if sample not in sample_map:
                    sample_map[sample] = [file_name]
                else:
                    sample_map[sample].append(file_name)
        except:
            pass
    for duplicates in sample_map.values():
        if len(duplicates) > 1:
            yield duplicates


def compare_samples(size, file_list):
    '''Compare a list of files having same size and search for possible duplicates.

    Duplicates generated by this function may NOT be duplicates.
    This may produce false positive results. But this will not produce false negative results.
    i.e. if this separates files as non-duplicate, they are actually non-duplicates.

    Number of sample checks is dependent on the size.

    :param size: Size of each file in file_list (all files should have same size)
    :param file_list: List of file names
    :returns: Generator for possibly duplicate files
    '''
    if size <= 50:
        yield file_list
        return
    for samp_5 in sample_util(size, file_list, 5):
        if size < 5000:
            yield samp_5
            continue
        for samp_31 in sample_util(size, samp_5, 31):
            if size < 10000000:
                yield samp_31
                continue
            for samp_101 in sample_util(size, samp_31, 101):
                yield samp_101


def compare_sizes(root, MIN_SIZE=0):
    '''Scan a directory and all its subdirectories for same sized files.

    Files smaller than MIN_SIZE are not included in the search.
    Generated file lists are in descending order of file size.

    :param root: Directory root to be scanned
    :param MIN_SIZE: Minimum size of files to be checked
    :returns: Generator for possibly duplicate files
    '''
    # dictionary with file size as key and list file names as value
    size_dict = dict()
    try:
        for l in walk(root):
            files = l[2]  # list of file names in the directory
            for file_name in files:
                p = path.join(l[0], file_name)
                if path.islink(p):
                    continue
                size = path.getsize(p)  # size of file
                if MIN_SIZE <= size:
                    if size in size_dict:  # if that size is already available
                        size_dict[size].append(p)
                    else:
                        size_dict[size] = [p]
    except KeyboardInterrupt:
        pass

    # sort by size. Largest first
    sizes = sorted(size_dict.keys(), reverse=True)
    for size in sizes:
        dup_size_list = size_dict.pop(size)
        if len(dup_size_list) > 1:
            yield (size, dup_size_list)


def duplicate_remove(root, MIN_SIZE=-1):
    root_len = len(root)
    # iterate through duplicate lists and
    # prompt user to select which files to remove
    try:
        for size, size_dup in compare_sizes(root, MIN_SIZE=MIN_SIZE):
            for sample_dup in compare_samples(size, size_dup):
                for duplicates in compare_files(sample_dup):
                    print("Size = %i bytes" % size)
                    for i in range(len(duplicates)):
                        # print 1 based indices
                        print("%i) %s" % (i+1, duplicates[i][root_len:]))
                    print()
                    try:
                        remove_list = tuple(map(int, input(
                            "Enter space separated list of indices to remove : ").strip().split()))
                        for index in remove_list:
                            index -= 1  # convert to 0 based index
                            if 0 <= index < len(duplicates):
                                remove(duplicates[index])
                    except ValueError:
                        pass
                print("\n")
    except KeyboardInterrupt:
        pass


root = input("Enter path : ")
duplicate_remove(root, 1)
