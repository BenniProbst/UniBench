import os
import re
from pathlib import Path


class LineSaver:
    target_file = os.path.expanduser("~") + '/noname.UniBench_config'
    in_memory = []

    def __init__(self, t_f):
        self.target_file = t_f + '.UniBench_config'
        parentinator = Path(self.target_file).parent
        working_dir = str(parentinator)
        if not os.path.isdir(working_dir):
            os.makedirs(working_dir)
        if not os.path.isfile(self.target_file):
            with open(self.target_file, 'w+') as f:
                f.writelines(self.in_memory)
        self.load_from_file()

    def load_from_file(self):  # discard changes
        with open(self.target_file, 'r') as f:
            self.in_memory = f.readlines()
        mem_refresh = []
        for m in self.in_memory:
            m = m.strip('\n')
            mem_refresh.append(m)
        self.in_memory = mem_refresh
        return self.in_memory

    def write_back(self):
        with open(self.target_file, 'w+') as f:
            for m in self.in_memory:
                m = m.strip('\n')
                f.write(m + '\n')
        return self.in_memory

    def load_from_memory(self):
        return self.in_memory

    def save_to_memory(self, listing):
        self.in_memory = listing

    def append(self, thing):
        self.in_memory = self.load_from_file()
        # if len(self.in_memory) == 1 and self.in_memory[0] == '':
        # self.in_memory = []
        self.in_memory.append(thing)
        self.write_back()

    def append_list(self, listing):
        self.in_memory = self.load_from_file()
        # if len(self.in_memory) == 1 and self.in_memory[0] == '':
        # self.in_memory = []
        for i in listing:
            self.in_memory.append(i)
        self.write_back()

    def insert(self, thing, index):
        self.in_memory = self.load_from_file()
        # if len(self.in_memory) == 1 and self.in_memory[0] == '':
        # self.in_memory = []
        self.in_memory.insert(index, thing)
        self.write_back()

    def rem(self, com):
        self.in_memory = self.load_from_file()
        self.in_memory.remove(com)
        # if len(self.in_memory) == 0:
        # .in_memory = ['']
        self.write_back()

    def remove_list(self, listing):
        self.in_memory = self.load_from_file()
        for i in listing:
            self.in_memory.remove(i)
        # if len(self.in_memory) == 0:
        # self.in_memory = ['']
        self.write_back()

    def is_empty(self):
        if len(self.load_from_file()) == 0:
            return True
        else:
            return

    def reset(self):
        self.in_memory = []
        self.write_back()

    def exists(self, cmd):
        self.in_memory = self.load_from_file()
        if cmd in self.in_memory:
            return True
        else:
            return False


class SelectableLineSaver(LineSaver):
    target_run = os.path.expanduser("~") + '/noname.UniBench_config_run'
    in_memory_run = '0'

    def __init__(self, t_f):
        super().__init__(t_f)
        self.target_run = t_f + '.UniBench_config_run'
        if not os.path.isfile(self.target_run):
            with open(self.target_run, 'w+') as f:
                f.write(self.in_memory_run)
        self.load_from_file_run()

    def help(self):
        print('AUTOMATION COMMAND - HELP CENTER:')
        print('add \"command\" - add an executable command line')
        print('add \"command\";\"command\",... - add multiple executable command lines')
        print('remove index - remove an executable command line from list above')
        print('remove index,index,... - remove multiple executable command lines from list above.')
        print('insert index \"command\" - inserts command at an index spot')
        print('replace index \"command\" - removes and inserts command at an index spot')
        print('save_run index,index,... - save run order of commands above, save 0 to run nothing')
        print('exit - exit git revision setup')
        print('help - print help once again\n')

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
        if self.in_memory_run == '0':
            print('No saved run order. Please configure!')
        else:
            print('\n')
            print('Run order:')
            print(self.in_memory_run)

    def add(self, com):
        st = com[4:]
        multi_com = st.split(';')
        count = 1 + len(self.in_memory)
        for m in multi_com:
            self.append(m)
            self.append_run(count)
            count += 1
        return self.in_memory

    def remove_config(self, com):
        st = com[7:]
        multi_com = st.split(',')
        for m in multi_com:
            to_del = int(m)
            self.remove_run(to_del)
            self.rem(self.load_from_file()[to_del - 1])
        return self.in_memory

    def insert_config(self, com):
        st = com[7:]
        split_cmd = st.split(' ')
        index = int(split_cmd[0])
        command_only = st[(len(str(index)) + 1):]
        if not self.exists(self.load_from_file()[index - 1]):
            print('The selected insert command was not found! No changes done.')
            return self.in_memory
        self.insert(command_only, index - 1)
        split_mem_run = [int(i) for i in self.load_from_file_run().split(',')]
        self.in_memory_run = '0'
        self.write_back_run()
        for i in split_mem_run:
            if i >= index:
                i += 1
            self.append_run(i)

    def replace_config(self, com):
        st = com[8:]
        index = int(st.split(' ')[0])
        command_only = st[(len(str(index)) + 1):]
        if not self.exists(self.load_from_file()[index - 1]):
            print('The selected replace command was not found! No changes done.')
            return self.in_memory
        self.rem(self.load_from_file()[index - 1])
        self.insert(command_only, index - 1)

    def save_run(self, com):
        re.compile('^[0-9]+(,[0-9]+)*$')
        char_ref = re.findall('[0-9]+', com)
        valid = True
        for c in char_ref:
            if int(c) > len(self.in_memory) or int(c) < 0:
                valid = False
                break
        if valid:
            self.in_memory_run = ",".join(char_ref)
        else:
            print('The sequence you\'ve entered contains invalid references! No changes committed.')
        self.write_back_run()

    def configure(self, cmd_list):
        count = 1
        for c in cmd_list:
            self.append(c)
            self.append_run(count)
            count += 1
        self.help()
        self.status()
        while True:
            com = input('Configuration command: ')
            if com.startswith('add'):
                try:
                    self.add(com)
                    self.status()
                except Exception:
                    print('Adding command(s) failed!')
            elif com.startswith('remove'):
                try:
                    self.remove_config(com)
                    self.status()
                except Exception:
                    print('Removing command(s) failed!')
            elif com.startswith('insert'):
                try:
                    self.insert_config(com)
                    self.status()
                except Exception:
                    print('Removing command(s) failed!')
            elif com.startswith('replace'):
                try:
                    self.replace_config(com)
                    self.status()
                except Exception:
                    print('Removing command(s) failed!')
            elif com.startswith('save_run'):
                try:
                    self.save_run(com)
                    self.status()
                except Exception:
                    print("Could not read the sequence!")
            elif com.startswith('exit'):
                break
            elif com.startswith('help'):
                self.help()
            else:
                print('Invalid command! Please try again...')

    def load_from_file_run(self):  # discard changes
        with open(self.target_run, 'r') as f:
            self.in_memory_run = f.readlines()[0].strip('\n')
        return self.in_memory_run

    def write_back_run(self):
        with open(self.target_run, 'w+') as f:
            f.writelines([self.in_memory_run])
        return self.in_memory_run

    def load_from_memory_run(self):
        return self.in_memory_run

    def save_to_memory_run(self, listing):
        self.in_memory_run = listing

    def append_run(self, number):
        self.load_from_file_run()
        if self.in_memory_run == '0':
            self.in_memory_run = ''
        if len(self.in_memory_run) == 0:
            self.in_memory_run += str(number)
        else:
            self.in_memory_run += ',' + str(number)
        self.write_back_run()
        return self.in_memory_run

    def insert_run(self, number, index):
        self.in_memory_run = self.load_from_file_run()
        if index > len(self.in_memory_run.split(',')):
            print('insert_run: Index out of range! No changes committed.')
            return self.in_memory_run
        if self.in_memory_run == '0':
            self.in_memory_run = ''
        if len(self.in_memory_run) == 0:
            self.in_memory_run += str(number)
        else:
            self.in_memory_run += ',' + str(number)
        change_list = self.in_memory_run.split(',')
        change_list[int(index)] = number
        self.in_memory_run = ''
        count = 0
        for m in change_list:
            if count == 0:
                self.in_memory_run += str(m)
            else:
                self.in_memory_run += ',' + str(m)
            count += 1
        self.write_back_run()
        return self.in_memory_run

    def remove_run(self, index):
        self.in_memory_run = self.load_from_file_run()
        split_mem = self.in_memory_run.split(',')
        if int(index) > len(self.in_memory):
            print('remove_run: Index out of range! No changes committed.')
            return self.in_memory_run
        run_numbers = []
        run_numbers_filtered = []
        for r in split_mem:
            if int(r) != index:
                run_numbers.append(int(r))
        for n in run_numbers:
            if n >= index:
                run_numbers_filtered.append(n - 1)
        self.save_to_memory_run('0')
        self.write_back_run()
        for n in run_numbers_filtered:
            self.append_run(n)
        return self.in_memory_run

    def is_empty_run(self):
        if self.is_empty() or self.load_from_file_run() == '0':
            return True
        else:
            return False

    def reset_run(self):
        self.reset()
        self.in_memory_run = '0'
        self.write_back_run()

    def exists_run(self, number):
        self.in_memory_run = self.load_from_file_run()
        if str(number) in self.in_memory_run.split(','):
            return True
        else:
            return False
