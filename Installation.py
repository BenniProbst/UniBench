import os


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
