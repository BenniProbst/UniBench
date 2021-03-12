import os
from pathlib import Path
import pickle


class LineSaver:
    target_file = Path(os.path.expanduser("~") + '/noname.UniBench_config')
    in_memory = []

    def __init__(self, t_f):
        self.target_file = Path(t_f + '.UniBench_config')
        working_dir = Path(os.path.dirname(self.target_file.absolute()))
        if not os.path.isdir(working_dir):
            os.makedirs(working_dir)
        if not os.path.isfile(self.target_file):
            with open(self.target_file, 'w') as f:
                pickle.dump(self.in_memory, f)
        self.in_memory = self.load_from_file()

    def load_from_file(self):  # discard changes
        with open(self.target_file, 'rb') as f:
            self.in_memory = pickle.load(f)
        return self.in_memory

    def write_back(self):
        with open(self.target_file, 'wb') as f:
            pickle.dump(self.in_memory, f)
        return self.in_memory

    def load_from_memory(self):
        return self.in_memory

    def save_to_memory(self, listing):
        self.in_memory = listing

    def append(self, thing):
        self.in_memory = self.load_from_file()
        self.in_memory.append(thing)
        self.write_back()

    def append_list(self, listing):
        self.in_memory = self.load_from_file()
        for i in listing:
            self.in_memory.append(i)
        self.write_back()

    def insert(self, thing, index):
        self.in_memory = self.load_from_file()
        self.in_memory.insert(index, thing)
        self.write_back()

    def remove(self, index):
        self.in_memory = self.load_from_file()
        self.in_memory.remove(index)
        self.write_back()

    def remove_list(self, listing):
        self.in_memory = self.load_from_file()
        for i in listing:
            self.in_memory.remove(i)
        self.write_back()
