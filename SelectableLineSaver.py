import LineSaver
from pathlib import Path
import pickle
import os


class SelectableLineSaver(LineSaver):
    target_run = Path(os.path.expanduser("~") + '/noname.UniBench_config_run')
    in_memory_run = ['']

    def __init__(self, t_f):
        super().__init__(self, t_f)
        self.target_run = Path(t_f + '.UniBench_config_run')
        if not os.path.isfile(self.target_run):
            with open(self.target_run, 'w') as f:
                pickle.dump(self.in_memory_run, f)
        self.in_memory_run = self.load_from_file_run()

    def help(self):
        print('HELP:')
        print('add \"command\" - add an executable command line')
        print('remove index - remove an executable command line from list above')
        print('add \"command\",\"command\",... - add multiple executable command lines')
        print('remove index,index,... - remove multiple executable command lines from list above.')
        print('save_run index,index,... - save run order of commands above, save 0 to run nothing')
        print('run - run configured command order')
        print('help - print help once again')

    def status(self):
        self.load_from_file()
        self.load_from_file_run()
        if len(self.in_memory) == 0:
            print('No saved selectable commands. Please configure!')
        else:
            print("Saved commands:")
            count = 1
            for i in self.in_memory:
                print(str(count) + ': \"' + str(i) + '\"')
                count += 1
        if len(self.in_memory_run) == 0:
            print('No saved run order. Please configure!')
        else:
            print('\n')
            print('Run order:')
            print(self.in_memory_run[0])

    def configure(self, cmd_list):
        count = 1
        for c in cmd_list:
            self.append(c)
            if len(self.in_memory_run[0]) == 0:
                self.in_memory_run[0] += str(count)
            else:
                self.in_memory_run[0] += ',' + str(count)
            count += 1
        self.write_back_run()
        self.help()
        self.status()
        while True:
            com = input('Configuration command: ')
            if com.startswith('add'):
                pass
            elif com.startswith('remove'):
                pass
            elif com.startswith('save_run'):
                pass
            elif com.startswith('run'):
                pass
            elif com.startswith('help'):
                pass
            else:
                print('Invalid command!')

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
