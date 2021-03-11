import os
import getpass


class Install:
    def __init__(self):
        program_name = input('Program main folder name:')
        print(
            'Give me the installation path where your program main folder should be installed to; press enter for '
            'default.')
        install_dir = '/home/' + str(getpass.getuser())
        print('Default:' + install_dir)
        new_dir = input("Installation directory:")
        tmp_dir = install_dir + '/' + program_name
        while len(new_dir) > 0 and not os.path.isdir(new_dir):
            print("An Error occured. This may not be a valid path! Please try again.")
            new_dir = input('Installation directory:')
            if len(new_dir) == 0:
                new_dir = install_dir
            if new_dir.endswith('/'):
                new_dir = new_dir[:-1]
            tmp_dir = new_dir + '/' + program_name
        # install_config = FileLineController(tmp_dir,program_name + '.i_config')
        # .i_run configuration
        # print('Python Morpheus installation script:')
        # os.system(
        #  "sudo apt-get install g++ cmake cmake-curses-gui xsltproc libxml2-utils doxygen git zlib1g-dev libboost-dev "
        #  "libboost-program-options-dev libtiff5-dev libsbml5-dev qttools5-dev libqt5svg5-dev qtwebengine5-dev "
        #  "libqt5sql5-sqlite gnuplot  ")
