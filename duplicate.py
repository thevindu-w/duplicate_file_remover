from os import path, walk, remove
import hashlib

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
            duplicates = dict()
            for file_name in l:
                try:
                    sha256 = hashlib.sha256()
                    with open(file_name, 'rb') as file:
                        while True:
                            buffer = file.read(4096)
                            if not buffer:
                                break
                            sha256.update(buffer)
                        digest = sha256.digest() # get SHA256 digest of the file
                        if digest not in duplicates:
                            duplicates[digest] = [file_name] # a list with one element
                        else:
                            duplicates[digest].append(file_name) # another file with same digest => duplicate
                except: pass

            #remove file names with no duplicates
            keys = tuple(duplicates.keys())
            for digest in keys:
                if len(duplicates[digest]) == 1:
                    duplicates.pop(digest)

            # iterate through duplicate lists and
            # prompt user to select which files to remove
            for digest in duplicates:
                print("Size = %i bytes"%size)
                dup_list = duplicates[digest]
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
