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

def create_inverted_indexes_list(files, genre):
    inverted_indexes = []

    for index, file in enumerate(files):
        lines = retrieve_file_content("./Movies/{}/{}".format(genre, file))
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

def create_chart(files, posting_list, index, genre):
    percentage = (len(posting_list[index][1]) * 100) / len(files)

    print("Word \"{}\" appears in {:0.2f}% of {} movie scripts ({} scripts out of {}).".format(posting_list[index][0], percentage, genre, str(len(posting_list[index][1])), str(len(files))))
    print("Appears in: ")
    for index in range(0, len(posting_list[index][1])):
        print("\t" + files[index][:-4])


def main():

    start_time = time.time()
    action_files = sorted(retrieve_files("./Movies/Action/"), key=str.lower)
    animation_files = sorted(retrieve_files("./Movies/Animation/"), key=str.lower)
    
    action_inverted_indexes = sorted(create_inverted_indexes_list(action_files, "Action"), key=lambda word: (word[0], word[1]))
    # print(*action_inverted_indexes, sep="\n")
    action_posting_list = ban_stop_words(create_posting_list(action_inverted_indexes))
    # print(*action_posting_list, sep="\n")

    animation_inverted_indexes = sorted(create_inverted_indexes_list(animation_files, "Animation"), key=lambda word: (word[0], word[1]))
    # print(*animation_inverted_indexes, sep="\n")
    animation_posting_list = ban_stop_words(create_posting_list(animation_inverted_indexes))
    # print(*animation_posting_list, sep="\n")

    # Quit now if debug mode is on
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        return

    print("--- %.2f seconds for movies indexing ---" % (time.time() - start_time))
    query = input("Select word: ")
    query = (query.strip()).lower()

    start_time = time.time()

    action_index = word_index(action_posting_list, query)
    animation_index = word_index(animation_posting_list, query)
    if action_index < 0 and animation_index < 0:
        print("Query word couldn't be found in any scripts")
        print("--- %.2f seconds for finding indexes ---" % (time.time() - start_time))
        return
    elif action_index < 0:
        print("Query word couldn't be found in any action movies")
        print("--- %.2f seconds for finding indexes ---" % (time.time() - start_time))
        return
    elif animation_index < 0:
        print("Query word couldn't be found in any animation movies")
        print("--- %.2f seconds for finding indexes ---" % (time.time() - start_time))
        return

    create_chart(action_files, action_posting_list, action_index, "Action")
    create_chart(animation_files, animation_posting_list, animation_index, "Animation")
    print("--- %.2f seconds for finding indexes ---" % (time.time() - start_time))

if __name__== "__main__" :
    main()