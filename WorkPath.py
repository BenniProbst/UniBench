import os
import getpass


class WorkPath:
    tmp_dir = ""

    def __init__(self):
        install_dir = '/home/' + str(getpass.getuser())
        print('Default:' + install_dir)
        new_dir = input("Work directory:")
        tmp_dir = install_dir
        while len(new_dir) > 0 and not os.path.isdir(new_dir):
            print("An Error occured. This may not be a valid path!")
            print(new_dir)
            create = ''
            while create != 'y' or create != 'n':
                create = input('Do you want to create this path? (y/n)')
                if create == 'y':
                    try:
                        os.makedirs(new_dir)
                        tmp_dir = new_dir
                    except FileExistsError:
                        print('File could not be created! Try again...')
                        continue
                elif create == 'n':
                    pass
                else:
                    continue
            if create == 'n':
                continue
            new_dir = input('New installation directory:')
            if len(new_dir) == 0:
                new_dir = install_dir
            if new_dir.endswith('/'):
                new_dir = new_dir[:-1]
            tmp_dir = new_dir
