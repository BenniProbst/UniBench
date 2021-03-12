import subprocess
import getpass
import os
import LineSaver
from pathlib import Path
import WorkPath


class Revision:
    revision_setups = None
    working_directory = None

    def revision_setup(self, program_url, username, password, project_path, project_name):
        self.revision_setups.append(project_path)
        while True:
            git_branch = input('Git branch: ')
            git_code = input('Git revision SHA: ')
            if not os.path.isdir(project_path):
                os.makedirs(project_path)
            os.chdir(project_path)
            cmd1 = ['git', 'clone', '-n', program_url,
                    project_path + '/' + project_name + '-' + git_branch + '-' + git_code]
            cmd2 = ['git', 'checkout', git_code]
            process = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
            # SHA Ziel ordner und repository universell einrichten, dass es herunterlädt
            process.wait()
            out = []
            for line in process.stdout:
                out.append(line)
            process = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)
            process.wait()
            out = []
            for line in process.stdout:
                out.append(line)

            rep = input('Add another revision code for testing? (y/n)')
            while not (rep == 'y' or rep == 'n'):
                print('What did you say?')
                rep = input('Add another revision code for testing? (y/n)')
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
        self.working_directory = work_dir
        saver_path = Path(str(Path(work_dir).absolute()) + '/revision_setups.UniBench_config')
        self.revision_setups = LineSaver.LineSaver(saver_path)
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
            project_path = self.working_directory + '/' + project_name
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
                    project_path = WorkPath.WorkPath('project').out()
                    if not os.path.isdir(project_path):
                        print('An Error occured! Project path could not be set. Please try again!')
                        project_path = self.working_directory + '/' + project_name
                        use_default_project_name = ''

            self.revision_setup(program_url, username, password, project_path, project_name)
            rep = input('Add another revision source? (y/n)')
            while not (rep == 'y' or rep == 'n'):
                print('What did you say?')
                rep = input('Add another revision source? (y/n)')
            if rep == 'n':
                break
