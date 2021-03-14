import os


# from subprocess import PIPE, Popen, STDOUT
# import re


class Installation:
    def __init__(self, new_dir):
        program_name = ''
        while len(program_name) == 0:
            program_name = input('Program main folder name:')
            if len(program_name) == 0:
                print('Program name was empty!')
        tmp_dir = new_dir + '/' + program_name
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        # install_config = FileLineController(tmp_dir,program_name + '.i_config')
        # .i_run configuration
        # print('Python Morpheus installation script:')
        # os.system(
        #  "sudo apt-get install g++ cmake cmake-curses-gui xsltproc libxml2-utils doxygen git zlib1g-dev libboost-dev "
        #  "libboost-program-options-dev libtiff5-dev libsbml5-dev qttools5-dev libqt5svg5-dev qtwebengine5-dev "
        #  "libqt5sql5-sqlite gnuplot  ")

    '''
    def exec(self, com_nr, respond_keys):
        cmd = (self.load_from_file()[com_nr]).split(' ')
        process = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        process.wait()
        out = []

        while True:
            for line in process.stdout:
                out.append(line)
            if len(out) == 0:
                break
            for key in respond_keys:
                if out[0].startswith(key):
                    out = []
                    process.communicate(input=respond_keys[key] + '\n')
                    process.wait()
                    break

        com = 'input'

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
    '''
