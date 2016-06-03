#! /usr/bin/python3

from os import listdir
from os.path import isfile, join

from research.main import generate_spectrum

input_path = "./data/input/"
etalon_path = "./data/etalons/"


def get_files(folder):
    return [join(folder, file) for file in listdir(folder) if isfile(join(folder, file))]


def get_spectrum_error(first, second):
    return sum([abs(first[i] - second[i]) for i in range(min(len(first), len(second)))])


# load etalons
etalon_files = get_files(etalon_path)
etalon_map = {}
for etalon_file in etalon_files:
    extension_position = etalon_file.find(".wav")
    letter = etalon_file[extension_position - 1: extension_position]
    etalon_map[letter] = generate_spectrum(etalon_file)

# load files to recognize
input_files = get_files(input_path)
for file in input_files:
    spectrum = generate_spectrum(file)

    min_error = float("inf")
    answer = ""
    for letter, etalon_spectrum in etalon_map.items():
        current_error = get_spectrum_error(spectrum, etalon_spectrum)
        if current_error < min_error:
            min_error = current_error
            answer = letter

    print("Letter in file {0} is {1}".format(file, answer))
