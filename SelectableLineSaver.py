import LineSaver
from pathlib import Path
import pickle
import os


class SelectableLineSaver(LineSaver):
    target_run = Path(os.path.expanduser("~") + '/noname.UniBench_config_run')
    in_memory_run = []

    def __init__(self, t_f):
        super().__init__(self, t_f)
        self.target_run = Path(t_f + '.UniBench_config_run')
        if not os.path.isfile(self.target_run):
            with open(self.target_run, 'w') as f:
                pickle.dump(self.in_memory_run, f)
        self.in_memory_run = self.load_from_file_run()

    def help(self):
        print('HELP:')
        print('add \"command\" - add an executeable command line')
        print('remove index - remove an executeable command line from list above')
        print('add \"command\",\"command\",... - add multiple executeable command lines')
        print('remove index,index,... - remove multiple executeable command lines from list above.')
        print('save_run index,index,... - save run order of commands above')
        print('run - run configured command order')

    def configure(self):
        self.help()

    def load_from_file_run(self):  # discard changes
        with open(self.target_file_run, 'r') as f:
            self.in_memory_run = pickle.load(f)
        return self.in_memory_run

    def write_back_run(self):
        with open(self.target_file_run, 'w+') as f:
            pickle.dump(self.in_memory_run, f)
        return self.in_memory_run

    def load_from_memory_run(self):
        return self.in_memory_run

    def save_to_memory_run(self, listing):
        self.in_memory_run = listing

    def append_run(self, thing):
        self.in_memory_run = self.load_from_file_run()
        self.in_memory_run.append(thing)
        self.write_back_run()

    def insert_run(self, thing, index):
        self.in_memory_run = self.load_from_file_run()
        self.in_memory_run.insert(index, thing)
        self.write_back_run()

    def remove(self, index):
        self.in_memory_run = self.load_from_file_run()
        self.in_memory_run.remove(index)
        self.write_back_run()
