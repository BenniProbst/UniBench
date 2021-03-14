import os

class WorkPath:
    tmp_dir = None

    def __init__(self, specific_type_string):
        print('---Workpath setup---')
        install_dir = os.path.expanduser("~")
        print(
            'Give me the installation path where your ' + specific_type_string + 'main folder(s) should be installed '
                                                                                 'to; press enter for '
                                                                                 'default setup.')
        print('Default:' + install_dir)
        new_dir = None
        while True:
            try:
                work_in = input("Working directory:")
                if len(work_in) == 0:
                    new_dir = None
                else:
                    new_dir = os.path.realpath(work_in)
                break
            except FileNotFoundError:
                print('Directory was not found!')
            except NotADirectoryError:
                print('The given path was not a directory!')
            except PermissionError:
                print('You do not have permissions to use anything here! Use the full path!')
            except Exception:
                print('Undefined Error!')
        while not (new_dir is None) and not os.path.exists(new_dir):
            print("An Error occured. This may not be a valid path!")
            print(new_dir)
            create = ''
            while not (create == 'y' or create == 'n'):
                create = input('Do you want to create this path? (y/n)')
                if create == 'y':
                    try:
                        os.makedirs(new_dir)
                    except FileNotFoundError:
                        print('Directory was not found!')
                        create = 'n'
                    except NotADirectoryError:
                        print('The given path was not a directory!')
                        create = 'n'
                    except PermissionError:
                        print('You do not have permissions to create anything here! Use the full path!')
                        create = 'n'
                    except Exception:
                        print('File could not be created! Try again...')
                        create = 'n'
                elif create == 'n':
                    break
                else:
                    continue
            if create == 'y':
                continue
            while True:
                try:
                    work_in = input("New installation directory:")
                    if len(work_in) == 0:
                        new_dir = None
                    else:
                        new_dir = os.path.realpath(work_in)
                    break
                except Exception:
                    print('Invalid Syntax! Please try again...')
            if new_dir is None:
                new_dir = install_dir
        if new_dir is None:
            new_dir = install_dir
        self.tmp_dir = new_dir
        print('Working directory: ' + self.tmp_dir)

    def out(self):
        return self.tmp_dir
