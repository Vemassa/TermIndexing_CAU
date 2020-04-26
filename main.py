import fileinput
from os import listdir
from os.path import isfile, join
import re
import time
import sys

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
            words = (line.lower()).split()
            inverted_indexes += list([word, index] for word in words)

    return inverted_indexes

def create_posting_list(list):
    posting_list = []
    i = 0

    while i < len(list):
        if i < 1:
            posting_list.append([list[i][0], [list[i][1]]])
        elif list[i][0] != list[i - 1][0]:
            posting_list.append([list[i][0], [list[i][1]]])
        elif list[i][1] not in posting_list[-1][1]:
            posting_list[-1][1].append(list[i][1])
        i += 1

    return posting_list

def ban_stop_words(posting_list):
    with open("stopwords.txt") as f_in:
        stopwords = (line.rstrip() for line in f_in)
        stopwords = list(line.strip() for line in stopwords if line)

    new_posting_list = [x for x in posting_list if x[0] not in stopwords]

    return (new_posting_list)

def word_index(posting_list, word):
    for index, elem in enumerate(posting_list):
        if word == elem[0]:
            return index
    return -1

def create_chart(files, posting_list, index):
    percentage = (len(posting_list[index][1]) * 100) / len(files)

    print("Word \"{}\" appears in {:0.2f}% of scripts ({} scripts out of {}).".format(posting_list[index][0], percentage, str(len(posting_list[index][1])), str(len(files))))
    print("Appears in: ")
    for index in range(0, len(posting_list[index][1])):
        print("\t" + files[index][:-4])


def main():

    files = sorted(retrieve_files("./Movies"), key=str.lower)
    inverted_indexes = sorted(create_inverted_indexes_list(files), key=lambda word: (word[0], word[1]))
    # print(*inverted_indexes, sep="\n")
    posting_list = ban_stop_words(create_posting_list(inverted_indexes))
    # print(*posting_list, sep="\n")

    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        return

    query = input("Select word: ")
    query = (query.strip()).lower()

    index = word_index(posting_list, query)
    if index < 0:
        print("Query word couldn't be found in any scripts")
        return

    create_chart(files, posting_list, index)

if __name__== "__main__" :
    main()