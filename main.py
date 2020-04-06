import fileinput
from os import listdir
from os.path import isfile, join
import re

def retrieve_files(folder):
    return [f for f in listdir(folder) if isfile(join(folder, f))]

def retrieve_file_content(filename):

    with open(filename) as f_in:
        lines = (line.rstrip() for line in f_in)
        lines = list(re.sub(r'[^A-Za-z0-9 ]+', '', line.strip()) for line in lines if line)

    return lines

def sort_indexes(list):
    return sorted(list, key=str.lower)

def posting_list(list):
    posting_list = []
    last_elem = ""
    i = 0

    while i < len(list):
        if i < 1:
            posting_list.append([list[i][0], 1, [list[i][1]]])
        elif list[i][0] != list[i - 1][0]:
            posting_list.append([list[i][0], 1, [list[i][1]]])
        elif list[i][1] not in posting_list[-1][2]:
            posting_list[-1][1] += 1
            posting_list[-1][2].append(list[i][1])
        i += 1

    # print(*posting_list, sep="\n")

def main():
    print("Hello, World!")

    files = retrieve_files("./Movies")
    inverted_indexes = []

    for index, file in enumerate(files):
        lines = retrieve_file_content("./Movies/" + file)
        for line in lines:
            words = line.split()
            inverted_indexes += list([word, index] for word in words)

    inverted_indexes = sorted(inverted_indexes, key=lambda word: (word[0], word[1]))
    posting_list(inverted_indexes)

    # print(*inverted_indexes, sep="\n")

if __name__== "__main__" :
    main()