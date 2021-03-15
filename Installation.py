import os
import LineSaver


# from subprocess import PIPE, Popen, STDOUT
# import re


class Installation:
    variations = {}
    static_configs = []
    variable_configs = []

    def __init__(self, work_dir, variation, config_filenames):
        self.variations = variation
        self.static_configs = config_filenames
        os.chdir(work_dir)
        revision_setups = LineSaver.LineSaver(work_dir + '/revision_setups')
        # check if config hierarchy is valid, if not, configure
        for setup in revision_setups.load_from_file():
            print('----Source installation and compilation manager----')
            print('Current project source: ' + setup)
            print('please configure how a project should be compiled or build!')
            print('Use the variable {revision} to reference to each combination of a revision folder\n')
            os.chdir(setup)
            revisions = setup + 'revisions'
            revision_line = LineSaver.LineSaver(revisions)
            print('Usage example: Type the thread modification command {threads} into the config file '
                  'and type the number of test threads into the last line of the document. The last line will be '
                  'treated differently and will not be executed. The input will be '
                  'recombined with all combinations possible above. If configuring multiple '
                  'variations separate argument types with \';\' in the order of their '
                  'registration list and separate variations to that argument type with '
                  '\',\'. The last line is never empty and requires at least one \';\' for an empty argument. The '
                  'argument past this argument, which does not end with semicolon as the only argument in the row is '
                  'setting up automation key phrases (optional). For example the shell will type the password after ['
                  'sudo], if ;{\"[sudo] \" : \"PW\"} was given in the last line. The shell detects prefixes. Hint use '
                  'static pads like {revisions}, created by the engine to create a combination over all the '
                  'information about the referenced configuration file. '
                  'Example before running the application: export '
                  'OMP_NUM_THREADS={threads} . Configuration in last line may look like '
                  'this: 2-6;{automation} or 1,2,3;{automation}')
            for rev in revision_line.load_from_file():
                print('SETTINGS TO FOLDER: ' + rev)
                self.variate_config(setup, rev)

        # recursively build suite file tree, the last recursion is a test this is done by building all replacement
        # files first into subdirectories, only copy global file one hierarchy down if there is not filename of that
        # type within the subdirectory. This gives us complete build variation lists in our revision folders with the
        # ending .variation_UniBench or better using memory a dict; multiline configs are separated with an empty
        # line with a semicolon on it. first build dict in memory with a file_name connected to the list,
        # what the file contains with copies of multiline commands, then work through static_configs, after that work
        # through variable_configs and go one recursion deeper each time you find a another variations file to iterate
        # over. Each recursion creates a master suite.
        # install phoronix-test-suite tests and suites automatically with a keymap by creating variate-compatible files
        # and finally run all tests and test suites
        # Read test results from database and copy all important ones into the .UniBench folder Morpheus repository

        os.chdir(work_dir)

    def variate_config(self, setup, rev_folder):
        print('---Variation manager---')
        for key in self.variations.keys():
            print('--' + key + '--')
            print('Hint: Delete individual configuration to use global project compilation settings! '
                  'Individual settings are dominant!')
            print('Replacement pad information: ' + self.variations[key]['replacements'])
            print('Replacement pads: ' + str(self.variations[key]['variation']))
            rep = input('Individual configuration? (y/n)')
            while not (rep == 'y' or rep == 'n'):
                print('What did you say?')
                rep = input('Individual configuration? (y/n)')
            compile_data = ''
            if rep == 'y':
                compile_data = rev_folder + '/' + self.variations[key]['file_name']
            else:
                compile_data = setup + '/' + self.variations[key]['file_name']
            compile_line = LineSaver.SelectableLineSaver(compile_data)
            compile_line.configure([])
            self.variable_configs.append(self.variations[key]['file_name'])

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
    
    login_keys = {'Username:': username, 'Password:': password}
    
    '''
