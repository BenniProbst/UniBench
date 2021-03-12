import os
from pathlib import Path


class WorkPath:
    tmp_dir = None

    def __init__(self):
        print('---Workpath setup---')
        install_dir = Path(os.path.expanduser("~"))
        print(
            'Give me the installation path where your program main folder(s) should be installed to; press enter for '
            'default setup.')
        print('Default:' + str(install_dir.absolute()))
        new_dir = Path(input("Work directory:"))
        while len(str(new_dir)) > 0 and not os.path.isdir(new_dir):
            print("An Error occured. This may not be a valid path!")
            print(new_dir)
            create = ''
            while not (create == 'y' or create == 'n'):
                create = input('Do you want to create this path? (y/n)')
                if create == 'y':
                    try:
                        os.makedirs(new_dir)
                    except Exception:
                        print('File could not be created! Try again...')
                        create = 'n'
                elif create == 'n':
                    break
                else:
                    continue
            if create == 'y':
                continue
            new_dir = Path(input('New installation directory:'))
            if len(str(new_dir)) == 0:
                new_dir = install_dir
        if len(new_dir) == 0:
            new_dir = install_dir
        self.tmp_dir = new_dir
        print('Working directory: ' + self.tmp_dir)

    def out(self):
        return self.tmp_dir
