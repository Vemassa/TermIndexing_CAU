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

def create_inverted_indexes_list(files):
    inverted_indexes = []

    for index, file in enumerate(files):
        lines = retrieve_file_content("./Movies/" + file)
        for line in lines:
            words = line.split()
            inverted_indexes += list([word, index] for word in words)

    return inverted_indexes

def create_posting_list(list):
    posting_list = []
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
    return posting_list

def ban_stop_words(posting_list):
    with open("stopwords.txt") as f_in:
        stopwords = (line.rstrip() for line in f_in)
        stopwords = list(line.strip() for line in stopwords if line)

    new_posting_list = [x for x in posting_list if x[0] not in stopwords]

    # print(*posting_list2, sep="\n")

    return (new_posting_list)

def main():
    print("Hello, World!")

    files = retrieve_files("./Movies")
    inverted_indexes = sorted(create_inverted_indexes_list(files), key=lambda word: (word[0], word[1]))
    posting_list = ban_stop_words(create_posting_list(inverted_indexes))

    print(*posting_list, sep="\n")

if __name__== "__main__" :
    main()