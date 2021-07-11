import os
import sys
import json, pickle
import pathlib  # do rozpoznawania rozszerzeń

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]


class FileHandler:
    def __init__(self):
        self.input_file = input_file_path  # nazwa pliku wchodzącego - drugi wyraz linii komend
        self.output_file = output_file_path  # plik wychodzący, który dopiero stworzymy
        self.list_of_changes = []  # lista modyfikacji podana w linii komend
        for change in sys.argv[3:]:  # wypełniamy listę modyfikacji w pętli
            self.list_of_changes.append(change.split(","))  # używamy splita, żeby rozdzielić części modyfikacji
        self.list_of_lines = []

    def __str__(self):
        return f'Input file: {self.input_file}; output file: {self.output_file}; changes: {self.list_of_changes}'

    def modify_file(self):
        for change in self.list_of_changes:  # pętla po wszystkich zmianach (każda zmiana to lista)
            if int(change[0]) > len(self.list_of_lines) - 1:  # jeśli podamy zbyt duzy Y
                return False
            if int(change[1]) > len(self.list_of_lines[0]) - 1:  # jeśli podamy zbyt duży X
                return False
            self.list_of_lines[int(change[0])][int(change[1])] = change[2]  # podmieniamy element listy
        return True


class CsvHandler(FileHandler):
    def __init__(self):
        super().__init__()
        self.read_file()

    def read_file(self):  # czyta i wstawia zawartość pliku do listy list (atrybutu klasy) lista[wiersz][element]
        list_of_lines = []
        with open(self.input_file, "r") as file:
            for line in file.readlines():
                separated_line = line.split("\n")[0].split(",")  # jedna linia (bez entera) w formie listy
                self.list_of_lines.append(separated_line)

    def save_file(self):
        with open(self.output_file, "w") as file:
            for line in self.list_of_lines:
                for element in line[:-1]:  # jedziemy po wszystkich elementach wiersza oprócz ostatniego
                    file.write(str(element) + ",")  # po każdym przecinek
                file.write(str(line[-1] + "\n"))  # a po ostatnim enter


class JsonHandler(FileHandler):
    def __init__(self):
        super().__init__()
        self.read_file()

    def read_file(self):
        with open(self.input_file, "r") as jsonfile:
            self.list_of_lines = json.load(jsonfile)  # w jaki sposób to się wczytuje? jaki tu zrobić atrybut?
                                               # oddzielny dla jsona, czy też listę list?

    def save_file(self):
        with open(self.output_file, "w") as jsonfile:
            json.dump(self.list_of_lines, jsonfile)


class PickleHandler(FileHandler):
    def __init__(self):
        super().__init__()
        self.read_file()

    def read_file(self):
        with open(self.input_file, "rb") as picklefile:
            self.list_of_lines = pickle.load(picklefile)

    def save_file(self):
        with open(self.output_file, "wb") as picklefile:
            pickle.dump(self.list_of_lines, picklefile)


def check_if_exists():
    if not os.path.exists(sys.argv[1]):
        return False
    return True


def show_directory():
    files = []
    for element in os.listdir('.'):
        if os.path.isfile(element):
            files.append(element)
    return files


def check_file_type(path):
    file_path = pathlib.PurePath(path)
    return file_path.suffix[1:]


def create_handler(path):
    extension = check_file_type(path)
    if extension == 'csv':
        reader = CsvHandler()
    elif extension == 'json':
        reader = JsonHandler()
    elif extension == 'pickle':
        reader = PickleHandler()
    else:
        return False
    return reader


# ------------------------------------------------------------------------
if not check_if_exists():
    print(f'No such file. Available files: {show_directory()}')
else:
    my_reader = create_handler(input_file_path)
    if not my_reader:
        print(f'We do not handle this filetype. Choose csv, json or pickle.')
    print(f'lista zmian: {my_reader.list_of_changes}')
    if not my_reader.modify_file():
        print(f'Change impossible - maximum index of row is {len(my_reader.list_of_lines) - 1} '
              f'and maximum index of column is {len(my_reader.list_of_lines[0]) - 1}')
    my_writer = create_handler(output_file_path)
    my_writer.list_of_lines = my_reader.list_of_lines
    my_writer.save_file()

