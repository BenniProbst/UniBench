import os
import getpass


class WorkPath:
    tmp_dir = ""

    def __init__(self):
        print('---Workpath setup---')
        install_dir = '/home/' + str(getpass.getuser())
        print(
            'Give me the installation path where your program main folder should be installed to; press enter for '
            'default.')
        print('Default:' + install_dir)
        new_dir = input("Work directory:")
        tmp_dir = install_dir
        while len(new_dir) > 0 and not os.path.isdir(new_dir):
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
            new_dir = input('New installation directory:')
            if len(new_dir) == 0:
                new_dir = install_dir
            if new_dir.endswith('/'):
                new_dir = new_dir[:-1]
        tmp_dir = new_dir
        print('Working directory: ' + tmp_dir)

    def out(self):
        return self.tmp_dir
