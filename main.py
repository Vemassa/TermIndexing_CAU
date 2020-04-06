import fileinput
from os import listdir
from os.path import isfile, join

def retrieve_files(folder):
    return [f for f in listdir(folder) if isfile(join(folder, f))]

def retrieve_file_content(filename):
    with open(filename) as f_in:
        lines = (line.rstrip() for line in f_in) 
        lines = list(line.strip() for line in lines if line)

    return lines

def main():
    print("Hello, World!")

    files = retrieve_files("./Movies")
    inverted_indexes = []

    for index, file in enumerate(files):
        lines = retrieve_file_content("./Movies/" + file)
        for line in lines:
            words = line.split()
            inverted_indexes += list([word, index] for word in words)


    print(*inverted_indexes, sep="\n")

if __name__== "__main__" :
    main()