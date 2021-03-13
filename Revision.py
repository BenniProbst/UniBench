import getpass
import os
import LineSaver
from pathlib import Path
import WorkPath
import shutil


class Revision:
    revision_setups_line = None
    working_directory = None

    def cmd_git(self, program_url, project_path, project_name, git_branch, git_code):
        # SHA Ziel ordner und repository universell einrichten, dass es herunterlädt
        commands = []
        cmd1 = 'git -C ' + project_path + '/' + project_name + '-' + git_branch + '-' + git_code + ' clone ' + \
               program_url
        commands.append(cmd1)
        cmd2 = 'git checkout ' + git_code
        commands.append(cmd2)
        return commands

    def revision_setup(self, program_url, username, password, project_path, project_name):
        if not os.path.isdir(project_path):
            print('Pfad existiert nicht und wird erstellt: \n' + project_path)
        if not os.path.isdir(project_path + '/' + project_name):
            print('Pfad existiert nicht und wird erstellt: \n' + project_path + '/' + project_name)
        self.revision_setups_line.append(project_path)
        if not os.path.isdir(project_path):
            os.makedirs(project_path)
        os.chdir(project_path)
        local_saver_path = Path(str(Path(project_path).absolute()) + '/revisions')
        revisions_line = LineSaver.LineSaver(local_saver_path)
        login_keys = {'Username:': username, 'Password:': password}
        while True:
            git_branch = input('Git branch: ')
            git_code = input('Git revision SHA: ')
            commands = self.cmd_git(program_url, project_path, project_name, git_branch, git_code)
            revision_output_folder = Path(str(project_path) + '/' + project_name + '-' + git_branch + '-' + git_code)
            if not os.path.isdir(revision_output_folder):
                os.makedirs(revision_output_folder)
            os.chdir(revision_output_folder)
            try:
                console_config = LineSaver.SelectableLineSaver(revision_output_folder)
                console_config.configure(commands, login_keys)
                revisions_line.append(revision_output_folder)
                os.chdir(project_path)
                rep = input('Add another revision code for testing? (y/n)')
                while not (rep == 'y' or rep == 'n'):
                    print('What did you say?')
                    rep = input('Add another revision code for testing? (y/n)')
                if rep == 'n':
                    break
            except Exception:
                print('Something went wrong! Deleting half finished revision folder!')
                os.chdir(project_path)
                shutil.rmtree(revision_output_folder)
                if len(revisions_line.load_from_memory()) > 0:
                    rep = input('To correct the error type \'y\', to exit type \'n\'. (y/n)')
                    while not (rep == 'y' or rep == 'n'):
                        print('What did you say?')
                        rep = input('To correct the error type \'y\', to exit type \'n\'. (y/n)')
                    if rep == 'n':
                        break

    def p_name(self, url):
        if str(url).endswith('.git'):
            url = str(url).removesuffix('.git')
        name = url.split("/")
        url = name[-1]
        if len(url) == 0:
            print('Failed to automatically retrieve project name, please set it now:')
            url = input('Manual project name: ')
        return url

    def __init__(self, work_dir):
        self.working_directory = Path(work_dir)
        saver_path = Path(str(Path(work_dir).absolute()) + '/revision_setups')
        self.revision_setups_line = LineSaver.LineSaver(saver_path)
        self.revision_setups_line.append(self.working_directory)
        print('-----Revision setup-----')
        print('WARNING: ALL GIVEN SOURCES (FOLDERS AND RECURSIVE FILES) WILL BE DELETED AN OVERWRITTEN TO UPDATE TEST '
              'PROPERTIES!!!')
        while True:
            print('----Online source setup----')
            print('Set platform login:')
            program_url = input('Git URL:')
            username = input('Target platform username: ')
            password = getpass.getpass(prompt='Target platform password: ')
            project_name = self.p_name(program_url)
            project_path = Path(str(self.working_directory.absolute()) + '/' + project_name)
            print('Default main project folder, named ' + project_name + ', where sub-revisions will be stored to:\n'
                  + project_path)
            use_default_project_name = input('Do you want to use the default path for revision enrollment inside of '
                                             'that directory? (y/n)')

            while not (use_default_project_name == 'y' or use_default_project_name == 'n'):
                print('What did you say?')
                print(
                    'Default main project folder, named ' + project_name + ', where sub-revisions will be stored to:\n'
                    + project_path)
                use_default_project_name = input('Do you want to use the default path for revision enrollment inside '
                                                 'of that directory? (y/n)')
                if use_default_project_name == 'n':
                    project_path = Path(WorkPath.WorkPath('project').out())
                    if not os.path.isdir(project_path):
                        print('An Error occured! Project path could not be set. Please try again!')
                        project_path = Path(str(self.working_directory.absolute()) + '/' + project_name)
                        use_default_project_name = ''

            self.revision_setup(program_url, username, password, project_path, project_name)
            rep = input('Add another revision source? (y/n)')
            while not (rep == 'y' or rep == 'n'):
                print('What did you say?')
                rep = input('Add another revision source? (y/n)')
            if rep == 'n':
                break
