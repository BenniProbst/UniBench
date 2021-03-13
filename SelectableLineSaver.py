import subprocess

import LineSaver
from pathlib import Path
import pickle
import os
import re


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

    def add(self, com):
        st = com.removeprefix('add ')
        multi_com = st.split(',')
        for m in multi_com:
            self.append(m.replace('\"', ''))
        return self.in_memory

    def remove_config(self, index_str):
        st = index_str.removeprefix('remove ')
        multi_com = st.split(',')
        for m in multi_com:
            to_del = int(m)
            self.remove(to_del)
            run_config = self.in_memory_run[0].split(',')
            run_numbers = []
            for r in run_config:
                if int(r) != to_del:
                    run_numbers.append(int(r))
            for n in run_numbers:
                if n >= to_del:
                    n -= 1
            self.in_memory_run[0] = ''
            self.write_back_run()
            for n in run_numbers:
                self.append_run(n)

    def save_run(self, com):
        re.compile('^[0-9]+(,[0-9]+)*$')
        char_ref = re.findall('[0-9]+', com)
        self.in_memory_run[0] = ",".join(char_ref)
        self.write_back_run()

    def exec(self, com_nr, respond_keys):
        cmd = self.load_from_file()
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        # SHA Ziel ordner und repository universell einrichten, dass es herunterlädt
        process.wait()
        out = []
        for line in process.stdout:
            out.append(line)

    def configure(self, cmd_list, respond_keys):
        count = 1
        for c in cmd_list:
            self.append(c)
            self.append_run(count)
            count += 1
        self.write_back_run()
        self.help()
        self.status()
        while True:
            com = input('Configuration command: ')
            if com.startswith('add'):
                try:
                    self.add(com)
                except Exception:
                    print('Adding command(s) failed!')
            elif com.startswith('remove'):
                try:
                    self.remove_config(com)
                except Exception:
                    print('Removing command(s) failed!')
            elif com.startswith('save_run'):
                try:
                    self.save_run(com)
                except Exception:
                    print("Could not read the sequence!")
            elif com.startswith('run'):
                try:
                    re.compile('^[0-9]+(,[0-9]+)*$')
                    char_ref = re.findall('[0-9]+', com)
                    for c in char_ref:
                        if c > len(self.in_memory):
                            raise ValueError
                    for c in char_ref:
                        self.exec(c, respond_keys)
                    break
                except ValueError:
                    print('A number could not be called from the list!')
                except Exception:
                    print("Configured Expression could not be run! Please reconfigure...")
            elif com.startswith('help'):
                self.help()
            else:
                print('Invalid command! Please try again...')

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

    def append_run(self, number):
        self.load_from_file_run()
        if len(self.in_memory_run[0]) == 0:
            self.in_memory_run[0] += str(number)
        else:
            self.in_memory_run[0] += ',' + str(number)
        self.write_back_run()

    def insert_run(self, thing, index):
        self.in_memory_run = self.load_from_file_run()
        self.in_memory_run.insert(index, thing)
        self.write_back_run()

    def remove_run(self, index):
        self.in_memory_run = self.load_from_file_run()
        self.in_memory_run.remove(index)
        self.write_back_run()
